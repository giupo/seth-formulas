from pathlib import Path
from seth.formula import Formula
from seth.types import BuildType

import shutil
import subprocess


RUN_SCRIPT = """#!/usr/bin/env bash
# Manages this keg's rserver as the current (non-root) user, single-user
# mode, with all runtime state kept under $DATA_DIR instead of /etc, /var
# and /run.
#
# Usage: rstudio-server-run [start|stop|status] [extra rserver flags...]
#   start (default) launches rserver in the background and prints its URL.
#   stop            stops the running instance.
#   status          reports whether it's running and where the log is.
#
# Port: RSTUDIO_PORT env var, or pass --www-port=... yourself (default 8787)
# Addr: RSTUDIO_ADDRESS env var (default 0.0.0.0 -- reachable from anywhere)
# R:    RSTUDIO_WHICH_R env var, or the first `R` found on PATH
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATA_DIR="${RSTUDIO_DATA_DIR:-$HOME/.local/seth/var/rstudio-server}"
OUT_FILE="$DATA_DIR/rserver.out"
mkdir -p "$DATA_DIR/run" "$DATA_DIR/varlib"

# rserver only writes --server-pid-file in daemonize mode; with
# --server-daemonize=0 (what we use, so we control backgrounding ourselves)
# it never writes one. So track it by matching the (unique, per-install)
# --server-data-dir on its command line instead of trusting a pidfile.
# bwrap (when used) does NOT forward signals to the sandboxed child, so
# 'stop' must target this real rserver pid, not the bwrap wrapper's.
MATCH="--server-data-dir=$DATA_DIR/run"
find_pid() {
  # pgrep -f also matches the bwrap wrapper (it carries rserver's whole
  # command line as its own argv), so filter down to the real rserver comm.
  local p
  for p in $(pgrep -f -- "$MATCH" 2>/dev/null); do
    if [ "$(cat "/proc/$p/comm" 2>/dev/null)" = "rserver" ]; then
      echo "$p"
      return 0
    fi
  done
  return 1
}

CMD="start"
case "${1:-}" in
  start|stop|status) CMD="$1"; shift ;;
esac

if [ "$CMD" = "status" ]; then
  pid="$(find_pid || true)"
  if [ -n "$pid" ]; then
    echo "rstudio-server: running (pid $pid), log: $OUT_FILE"
  else
    echo "rstudio-server: not running"
  fi
  exit 0
fi

if [ "$CMD" = "stop" ]; then
  pid="$(find_pid || true)"
  if [ -n "$pid" ]; then
    kill "$pid"
    echo "rstudio-server: stopped"
  else
    echo "rstudio-server: not running"
  fi
  exit 0
fi

pid="$(find_pid || true)"
if [ -n "$pid" ]; then
  echo "rstudio-server: already running (pid $pid). Use 'rstudio-server-run stop' first." >&2
  exit 1
fi

R_BIN="${RSTUDIO_WHICH_R:-$(command -v R || true)}"
if [ -z "$R_BIN" ]; then
  echo "rstudio-server-run: no R found. Install one (e.g. 'seth install R') or set RSTUDIO_WHICH_R." >&2
  exit 1
fi

# rserver spawns rsession with a minimal LD_LIBRARY_PATH (just $R_HOME/lib),
# but R's own launcher script computes a fuller one from $R_HOME/etc/ldpaths
# (e.g. it includes an MKL/OpenBLAS deps dir on builds that use one). Without
# it rsession dlopen()-fails on libR.so's own dependencies and crashes on
# every launch -- which just looks like "R is taking longer than usual" in
# the browser, forever. Ask R itself for the LD_LIBRARY_PATH it would use, so
# this works for whatever R is pointed at instead of hardcoding a BLAS path.
R_LD_LIBRARY_PATH="$("$R_BIN" --vanilla -s -e 'cat(Sys.getenv("LD_LIBRARY_PATH"))' 2>/dev/null || true)"

PORT="${RSTUDIO_PORT:-8787}"
ARGS=(
  --server-user="$(id -un)"
  --server-daemonize=0
  --server-working-dir="$HOME"
  --server-data-dir="$DATA_DIR/run"
  --secure-cookie-key-file="$DATA_DIR/secure-cookie-key"
  --rsession-config-file="$HERE/conf/rsession.conf"
  --database-config-file="$HERE/conf/database.conf"
  --auth-none=1
  --www-address="${RSTUDIO_ADDRESS:-0.0.0.0}"
  --rsession-which-r="$R_BIN"
)
case " $* " in
  *" --www-port="*|*" --www-port "*) ;;
  *) ARGS+=(--www-port="$PORT") ;;
esac
if [ -n "$R_LD_LIBRARY_PATH" ]; then
  case " $* " in
    *" --rsession-ld-library-path="*|*" --rsession-ld-library-path "*) ;;
    *) ARGS+=(--rsession-ld-library-path="$R_LD_LIBRARY_PATH") ;;
  esac
fi

# rserver hardcodes /var/lib/rstudio-server as its SQLite state directory;
# no --server-data-dir/env override reaches it (verified empirically against
# rstudio-server 2026.08.2-200). Redirect it into $DATA_DIR/varlib for this
# process only, via an unprivileged mount namespace, so no root is needed.
if [ -d /var/lib/rstudio-server ] && [ -w /var/lib/rstudio-server ]; then
  LAUNCH=("$HERE/bin/rserver" "${ARGS[@]}" "$@")
elif command -v bwrap >/dev/null 2>&1; then
  BW=(--bind / / --dev-bind /dev /dev --proc /proc --tmpfs /var/lib)
  for e in /var/lib/*; do
    [ "$(basename "$e")" = "rstudio-server" ] && continue
    BW+=(--bind "$e" "$e")
  done
  BW+=(--bind "$DATA_DIR/varlib" /var/lib/rstudio-server)
  LAUNCH=(bwrap "${BW[@]}" -- "$HERE/bin/rserver" "${ARGS[@]}" "$@")
else
  cat >&2 <<EOF
rstudio-server-run: /var/lib/rstudio-server does not exist (or isn't
writable by you) and 'bwrap' (bubblewrap) isn't available to sandbox
around it.

Ask an admin to run once (the directory can stay empty; it's only used
as a mount point):
  sudo mkdir -p /var/lib/rstudio-server
  sudo chown $(id -un) /var/lib/rstudio-server

Then re-run this script.
EOF
  exit 1
fi

setsid "${LAUNCH[@]}" </dev/null >"$OUT_FILE" 2>&1 &
disown

for _ in $(seq 1 20); do
  sleep 0.5
  pid="$(find_pid || true)"
  if [ -n "$pid" ]; then
    echo "rstudio-server: started on port $PORT (pid $pid)"
    echo "  reachable at: http://$(hostname -s 2>/dev/null || hostname):$PORT/  (use the address other hosts reach this machine on)"
    echo "  log: $OUT_FILE"
    echo "  stop with: rstudio-server-run stop"
    exit 0
  fi
done

echo "rstudio-server: failed to start -- see $OUT_FILE" >&2
tail -n 20 "$OUT_FILE" >&2 2>/dev/null || true
exit 1
"""


class RstudioServerFormula(Formula):
    name = "rstudio-server"
    latest = "2026.08.2-200"

    build_system = BuildType.CUSTOM

    versions = {
        "2026.08.2-200": {
            "url": "https://download2.rstudio.org/server/rhel8/x86_64/rstudio-server-rhel-2026.08.2-200-x86_64.rpm",
            "sha256": "e33b19ed3084fef4c4b9612d51f5277e6b9405d1899e56ca31655388ff34617c",
        },
    }

    def build(self, source_dir: Path):
        # extract() can't decompress an .rpm, so it just copied it as-is
        # into source_dir (see builder.extract's fallback branch). Unpack
        # the payload with rpm2cpio/cpio: no rpm install, no root needed.
        rpm_path = next(source_dir.glob("*.rpm"))

        payload_dir = source_dir / "payload"
        payload_dir.mkdir(exist_ok=True)
        rpm2cpio = subprocess.Popen(["rpm2cpio", str(rpm_path)], stdout=subprocess.PIPE)
        subprocess.run(["cpio", "-idm", "--quiet"], stdin=rpm2cpio.stdout, cwd=payload_dir, check=True)
        rpm2cpio.stdout.close()
        if rpm2cpio.wait() != 0:
            raise RuntimeError("rpm2cpio failed")

        payload = payload_dir / "usr" / "lib" / "rstudio-server"
        if self.keg.exists():
            shutil.rmtree(self.keg)
        shutil.copytree(payload, self.keg)

    def post_install(self):
        conf_dir = self.keg / "conf"
        conf_dir.mkdir(exist_ok=True)
        (conf_dir / "rserver.conf").touch()
        (conf_dir / "rsession.conf").touch()
        (conf_dir / "database.conf").touch()  # empty -> embedded SQLite

        wrapper = self.keg / "bin" / "rstudio-server-run"
        wrapper.write_text(RUN_SCRIPT)
        wrapper.chmod(0o755)
