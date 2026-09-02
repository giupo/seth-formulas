from seth.formula import Formula
from seth.types import BuildType
from pathlib import Path

class ClocFormula(Formula):
    name = "cloc"
    latest = "2.10"

    # dependencies = []
    # build_dependencies = []
    build_system = BuildType.CUSTOM

    versions = {
        "2.10": {
            "url": "https://github.com/AlDanial/cloc/releases/download/v2.10/cloc-2.10.pl",
            "sha256": "bf59272455172108072a0a106379f7509fd4349bdcfd85203bac038ccd286d83",
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
        import stat

        src = source_dir / "cloc-2.10.pl"
        dst_dir = self.keg / "bin"
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / "cloc"
        shutil.copy2(src, dst)
        dst.chmod(
            dst.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        )

    # def post_install(self):
    #     pass

