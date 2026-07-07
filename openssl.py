import os

from seth.formula import Formula


class OpenSSLFormula(Formula):
    name = "openssl"
    latest = "3.3.2"
    build_system = "custom"
    dependencies = ["zlib", "perl"]
    versions = {
        "3.3.2": {
            "url": "https://github.com/openssl/openssl/releases/download/openssl-3.3.2/openssl-3.3.2.tar.gz",
            "sha256": "2e8a40b01979afe8be0bbfb3de5dc1c6709fedb46d6c89c10da114ab5fc3d281",
        },
        "3.3.1": {
            "url": "https://github.com/openssl/openssl/releases/download/openssl-3.3.1/openssl-3.3.1.tar.gz",
            "sha256": "777cd596284c883375a2a7a11bf5d2786fc5413255efab20c50d6ffe6d020b7e",
        },
        "3.2.3": {
            "url": "https://github.com/openssl/openssl/releases/download/openssl-3.2.3/openssl-3.2.3.tar.gz",
            "sha256": "b7de5f5d09d4218e4f3a67e47d0ded0e32a48b86d26ca18f5ad694f1aa1e3ce0",
        },
    }

    def build(self, source_dir):
        nproc = os.cpu_count() or 1

        from seth.builder import get_build_env, run
        env = get_build_env()

        run([
            "./Configure",
            f"--prefix={self.keg}",
            f"--openssldir={self.keg}/ssl",
            "linux-x86_64",
            "shared",
            "zlib",
        ], cwd=source_dir, env=env)
        run(["make", f"-j{nproc}"], cwd=source_dir, env=env)
        run(["make", "install_sw"], cwd=source_dir, env=env)
