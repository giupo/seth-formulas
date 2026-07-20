from seth.formula import Formula
from seth.types import BuildType

class NpthFormula(Formula):
    name = "npth"
    latest = "1.8"

    # dependencies = []
    # build_dependencies = []
    # build_system = BuildType.AUTOCONF

    versions = {
        "1.8": {
            "url": "https://www.gnupg.org/ftp/gcrypt/npth/npth-1.8.tar.bz2",
            "sha256": "8bd24b4f23a3065d6e5b26e98aba9ce783ea4fd781069c1b35d149694e90ca3e",
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

