from seth.formula import Formula
from seth.types import BuildType

class GpgFormula(Formula):
    name = "gpg"
    latest = "2.5.21"

    dependencies = ["libgpg-error", "libgcrypt", "libksba", "libassuan", "ntbtls", "npth"]
    # build_dependencies = []
    # build_system = BuildType.AUTOCONF

    versions = {
        "2.5.21": {
            "url": "https://www.gnupg.org/ftp/gcrypt/gnupg/gnupg-w32-2.5.21_20260702.tar.xz",
            "sha256": "7e12add431c74358c2f3a73fd2d4caccabb33950fa79307fce43600ff5b50b18",
        },
    }

    # def configure_args(self) -> list[str]:
    #     return [
    #         f"--prefix={self.keg}",
    #         "--enable-shared",
    #     ]

    # def configure_args(self) -> list[str]:
    #     return [f"--prefix={self.keg}"] + self.extra_configure_args

    # def make_args(self) -> list[str]:
    #     """Variables/flags appended to every `make` invocation (e.g. CFLAGS=-O2)."""
    #     return self.extra_make_args

    # def cmake_args(self) -> list[str]:
    #     return [f"-DCMAKE_INSTALL_PREFIX={self.keg}"] + self.extra_configure_args

    # def meson_args(self) -> list[str]:
    #     return [f"--prefix={self.keg}"] + self.extra_configure_args

    # def patch(self, source_dir: Path):
    #     """Override for programmatic source modifications applied before build."""

    # def build(self, source_dir:Path):
    #     pass

    # def post_install(self):
    #     pass

