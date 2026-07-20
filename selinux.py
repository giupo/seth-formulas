from seth.formula import Formula
from seth.types import BuildType

class SelinuxFormula(Formula):
    name = "selinux"
    latest = "3.11"

    # dependencies = []
    # build_dependencies = []
    build_system = BuildType.MAKE

    versions = {
        "3.11": {
            "url": "https://github.com/SELinuxProject/selinux/releases/download/3.11/selinux-3.11.tar.gz",
            "sha256": "6b6d47ab0f35fe1c09bda0c62821c8d97a0cbe7f6e9404b338df7bde0182c4f4",
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

