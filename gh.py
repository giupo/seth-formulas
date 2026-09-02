from seth.formula import Formula
from seth.types import BuildType
from pathlib import Path

class GhFormula(Formula):
    name = "gh"
    latest = "2.98.0"

    # dependencies = []
    # build_dependencies = []
    build_system = BuildType.CUSTOM

    versions = {
        "2.98.0": {
            "url": "https://github.com/cli/cli/releases/download/v2.98.0/gh_2.98.0_linux_amd64.tar.gz",
            "sha256": "3b8ac6b30336802fc1a858d7c084e11cdf24ac1a761ca90b68022d7d729208de",
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
        self.keg.mkdir(parents=True, exist_ok=True)
        # for fuck sacke why leave LICENSE there?
        license = source_dir / "LICENSE"
        license.unlink()
        shutil.copytree(source_dir, self.keg, dirs_exist_ok=True)
         
    # def post_install(self):
    #     pass

