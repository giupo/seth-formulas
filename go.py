from seth.formula import Formula
from seth.types import BuildType
from pathlib import Path

class GoFormula(Formula):
    name = "go"
    latest = "1.27.0"

    # dependencies = []
    # build_dependencies = []
    build_system = BuildType.CUSTOM

    versions = {
        "1.27.0": {
            "url": "https://go.dev/dl/go1.27.0.linux-amd64.tar.gz",
            "sha256": "675c26c449cbb18fc24b74650de1eabbae6e16f64326fd85a283fb3b58280685",
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

    def build(self, source_dir:Path):
        import shutil
        dst_dir = self.keg
        dst_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_dir, dst_dir, dirs_exist_ok=True)

    # def post_install(self):
    #     pass

