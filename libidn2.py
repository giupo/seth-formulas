from seth.formula import Formula
from seth.types import BuildType

class Libidn2Formula(Formula):
    name = "libidn2"
    latest = "2.3.8"

    dependencies = ["libunistring"]
    # build_dependencies = []
    # build_system = BuildType.AUTOCONF

    versions = {
        "2.3.8": {
            "url": "https://ftpmirror.gnu.org/libidn/libidn2-2.3.8.tar.gz",
            "sha256": "f557911bf6171621e1f72ff35f5b1825bb35b52ed45325dcdee931e5d3c0787a",
        },
    }

    # def configure_args(self) -> list[str]:
    #     return [
    #         f"--prefix={self.keg}",
    #         "--enable-shared",
    #     ]

    def configure_args(self) -> list[str]:
        return [f"--prefix={self.keg}"] + self.extra_configure_args

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

