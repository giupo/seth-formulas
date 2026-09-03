import os
from pathlib import Path

from seth.formula import Formula
from seth.types import BuildType


class IntltoolFormula(Formula):
    """intltool: needed only as a build-time dependency of libgsf (its
    autotools build unconditionally requires AC_PROG_INTLTOOL, no matter
    what --disable-nls says).

    intltool-update/-merge/-extract are perl scripts that `use XML::Parser`.
    Rather than plumb PERL5LIB through every consumer, the small chain of
    pure-perl CPAN modules it needs (XML::Parser and its own build deps)
    are installed straight into the `perl` formula's own site directories
    below, so any script using that perl's shebang sees them with zero
    extra environment wiring - exactly like a normal `cpan install` would.
    """

    name = "intltool"
    latest = "0.51.0"
    dependencies = ["perl"]
    build_system = BuildType.CUSTOM

    versions = {
        "0.51.0": {
            "url": "https://archive.ubuntu.com/ubuntu/pool/main/i/intltool/intltool_0.51.0.orig.tar.gz",
            "sha256": "67c74d94196b153b774ab9f89b2fa6c6ba79352407037c8c14d5aeb334e959cd",
        },
    }

    # (dirname, url, sha256, extra Makefile.PL args) - installed in this order.
    _perl_modules = [
        (
            "Class-Inspector-1.36",
            "https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/Class-Inspector-1.36.tar.gz",
            "cc295d23a472687c24489d58226ead23b9fdc2588e522f0b5f0747741700694e",
            [],
        ),
        (
            "File-ShareDir-Install-0.14",
            "https://cpan.metacpan.org/authors/id/E/ET/ETHER/File-ShareDir-Install-0.14.tar.gz",
            "8f9533b198f2d4a9a5288cbc7d224f7679ad05a7a8573745599789428bc5aea0",
            [],
        ),
        (
            "File-ShareDir-1.118",
            "https://cpan.metacpan.org/authors/id/R/RE/REHSACK/File-ShareDir-1.118.tar.gz",
            "3bb2a20ba35df958dc0a4f2306fc05d903d8b8c4de3c8beefce17739d281c958",
            [],
        ),
        (
            "XML-Parser-2.59",
            "https://cpan.metacpan.org/authors/id/T/TO/TODDR/XML-Parser-2.59.tar.gz",
            "a358fd7c49f5e27717a644a9102bd21dc7fc25a415983279c59b1580e2b62a58",
            ["EXPATLIBPATH=/usr/lib64", "EXPATINCPATH=/usr/include"],
        ),
    ]

    def build(self, source_dir: Path):
        from seth.builder import get_build_env, run
        from seth.config import config

        nproc = os.cpu_count() or 1
        perl_ver = self.direct_deps.get("perl", "")
        perl_keg = config.cellar / "perl" / perl_ver
        perl_bin = perl_keg / "bin" / "perl"

        env = get_build_env(self.direct_deps)

        tmp_root = source_dir.parent / "perl-modules"
        tmp_root.mkdir(exist_ok=True)

        for dirname, url, sha256, extra_args in self._perl_modules:
            mod_root = tmp_root / dirname
            mod_dir = self._fetch_and_extract(url, sha256, mod_root)
            run([str(perl_bin), "Makefile.PL"] + extra_args, cwd=mod_dir, env=env)
            run(["make", f"-j{nproc}"], cwd=mod_dir, env=env)
            run(["make", "install"], cwd=mod_dir, env=env)

        run(["./configure", f"--prefix={self.keg}"], cwd=source_dir, env=env)
        run(["make", f"-j{nproc}"], cwd=source_dir, env=env)
        run(["make", "install"], cwd=source_dir, env=env)

    @staticmethod
    def _fetch_and_extract(url: str, sha256: str, dest_root: Path) -> Path:
        import hashlib
        import tarfile
        import urllib.request

        dest_root.mkdir(parents=True, exist_ok=True)
        archive = dest_root / url.split("/")[-1]
        urllib.request.urlretrieve(url, archive)

        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        if digest != sha256:
            raise ValueError(
                f"Checksum mismatch for {archive.name}\n"
                f"  expected: {sha256}\n  actual:   {digest}"
            )

        with tarfile.open(archive) as tf:
            tf.extractall(dest_root, filter="data")
        entries = [p for p in dest_root.iterdir() if p.is_dir()]
        return max(entries, key=lambda p: p.stat().st_mtime)
