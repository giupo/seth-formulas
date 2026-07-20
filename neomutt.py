from seth.formula import Formula
from seth.types import BuildType

class NeomuttFormula(Formula):
    name = "neomutt"
    latest = "2026-06-16"

    # dependencies = []
    build_dependencies = ["ncurses", "openssl", "lua"]
    # build_system = BuildType.AUTOCONF

    versions = {
        "2026-06-16": {
            "url": "https://github.com/neomutt/neomutt/archive/refs/tags/20260616.tar.gz",
            "sha256": "2c34fdd2166d5765e6bfdc21d1248bc4e92ddc0a33537b9418c17cd90e2dda80",
        },
    }

    # def configure_args(self) -> list[str]:
    #     return [
    #         f"--prefix={self.keg}",
    #         "--enable-shared",
    #     ]

    def configure_args(self) -> list[str]:
        from seth.config import config
        openssl_ver = self.direct_deps.get("openssl", "")
        openssl_root = config.cellar / "openssl" / openssl_ver / "lib"
        
        lua_ver = self.direct_deps.get("lua", "")
        lua_root = config.cellar / "lua" / lua_ver / "lib"

        return [
            f"--prefix={self.keg}",
            "--ssl",
            "--disable-doc",
            "--gpgme",
        ] + self.extra_configure_args

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

