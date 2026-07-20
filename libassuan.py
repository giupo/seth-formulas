from seth.formula import Formula
from seth.types import BuildType

class LibassuanFormula(Formula):
    name = "libassuan"
    latest = "3.0.2"

    # dependencies = []
    # build_dependencies = []
    # build_system = BuildType.AUTOCONF

    versions = {
        "3.0.2": {
            "url": "https://www.gnupg.org/ftp/gcrypt/libassuan/libassuan-3.0.2.tar.bz2",
            "sha256": "d2931cdad266e633510f9970e1a2f346055e351bb19f9b78912475b8074c36f6",
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

