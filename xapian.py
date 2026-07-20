from seth.formula import Formula
from seth.types import BuildType

class XapianFormula(Formula):
    name = "xapian"
    latest = "2.0.0"

    # dependencies = []
    # build_dependencies = []
    # build_system = BuildType.AUTOCONF

    versions = {
        "2.0.0": {
            "url": "https://oligarchy.co.uk/xapian/2.0.0/xapian-core-2.0.0.tar.xz",
            "sha256": "6cea3f49952a47224439a40bdb3608f928d121ad8721b9921cc42802d548ecf8"
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

