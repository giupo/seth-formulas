from seth.formula import Formula


class UtilLinuxFormula(Formula):
    name = "util-linux"
    latest = "2.4.2"
    dependencies = ["gettext"]
    # build_dependencies = []
    build_system="autogen"

    versions = {
        "2.4.2": {
            "url": "https://github.com/util-linux/util-linux/archive/refs/tags/v2.42.2.tar.gz",
            "sha256": "a451596f794739216da2e98398e31958ecf455f2372d99a12194a468e852e834"
        },
    }

    # def configure_args(self):
    #     return [
    #         f"--prefix={self.keg}",
    #         "--enable-shared",
    #     ]
