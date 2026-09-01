from seth.formula import Formula
from seth.types import BuildType

class CntlmFormula(Formula):
    name = "cntlm"
    latest = "0.94.3"

    # dependencies = []
    # build_dependencies = []
    build_system = BuildType.CMAKE

    versions = {
        "0.94.3": {
            "url": "https://github.com/giupo/cntlm-gss/releases/download/v0.94.3/cntlm-0.94.3-src.tar.gz",
            "sha256": "1c5562465ad37afe7e960b143e37975db46b34c13ef253144da96b28016b225f",
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

