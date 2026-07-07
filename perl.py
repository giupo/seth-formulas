import os

from seth.formula import Formula


class PerlFormula(Formula):
    name = "perl"
    latest = "5.40.0"
    build_system = "custom"
    dependencies = ["zlib"]

    versions = {
        "5.40.0": {
            "url": "https://www.cpan.org/src/5.0/perl-5.40.0.tar.gz",
            "sha256": "c740348f357396327a9795d3e8323bafd0fe8a5c7835fc1cbaba0cc8dfe7161f",
        },
    }

    def build(self, source_dir):
        from seth.builder import get_build_env, run
        from seth.config import config

        nproc = os.cpu_count() or 1
        zlib_ver = self.direct_deps.get("zlib", "")
        zlib_keg = config.cellar / "zlib" / zlib_ver

        configure_args = [
            "-des",
            f"-Dprefix={self.keg}",
            f"-Dvendorprefix={self.keg}",
            f"-Dsiteprefix={self.keg}",
            f"-Dman1dir={self.keg}/share/man/man1",
            f"-Dman3dir={self.keg}/share/man/man3",
            "-Duseshrplib",   # build shared libperl.so
            "-Dusethreads",   # thread support (required by many CPAN modules)
            "-Duselargefiles",
            "-Dcc=gcc",
        ]

        if zlib_keg.exists():
            configure_args += [
                f"-Dzlib-include={zlib_keg}/include",
                f"-Dzlib-lib={zlib_keg}/lib",
            ]

        # Configure is a perl/shell script; LC_ALL=C avoids locale-related
        # surprises in the probe output parsing.
        env = get_build_env(self.direct_deps)
        env.update({"LC_ALL": "C", "LANG": "C"})
        run(["sh", "Configure"] + configure_args, cwd=source_dir, env=env)
        run(["make", f"-j{nproc}"], cwd=source_dir, env=env)
        run(["make", "install"], cwd=source_dir, env=env)
