from seth.formula import Formula
from seth.types import BuildType

class GtkDocFormula(Formula):
    name = "gtk-doc"
    latest = "1.36.1"

    # dependencies = []
    # build_dependencies = []
    build_system = BuildType.MESON

    versions = {
        "1.36.1": {
            "url": "https://download.gnome.org/sources/gtk-doc/1.36/gtk-doc-1.36.1.tar.xz",
            "sha256": "0e517a5f97069831181be177516bde8aa8b3922398f2bdb09e265d22aecadbc5",
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

