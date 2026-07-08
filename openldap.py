from seth.formula import Formula
from seth.types import BuildType

class OpenldapFormula(Formula):
    name = "openldap"
    latest = "2.6.13"

    # dependencies = []
    # build_dependencies = []
    # build_system = BuildType.AUTOCONF

    versions = {
        "2.6.13": {
            "url": "https://github.com/openldap/openldap/archive/refs/tags/OPENLDAP_REL_ENG_2_6_13.tar.gz",
            "sha256": "dd5be2f8e7deab34d1afc3babb7ad29fd1391860b321ffdbcab4ed7a5dfccf76",
        },
    }

    def configure_args(self) -> list[str]:
         return [
             f"--prefix={self.keg}",
             "--enable-slapd",
             "--enable-mdb",
             "--with-tls=openssl",
             "--with-cyrus-sasl"
         ]

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

