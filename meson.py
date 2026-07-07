from seth.formula import Formula
from seth.builder import run

from pathlib import Path

import stat

class MesonFormula(Formula):
    name = "meson"
    latest = "1.11.1"
    dependencies = ["python"]
    # build_dependencies = []
    build_system = "custom"
    
    versions = {
        "1.11.1": {
            "url": "https://github.com/mesonbuild/meson/releases/download/1.11.1/meson-1.11.1.tar.gz",
            "sha256": "6788ae299979643f8d841bcaf64352558436cae45a0355148a3aeeccf7913866",
        },
    }
        
    def build(self, source_dir: Path):
        # packaging 
        
        run([
            "packaging/create_zipapp.py"
        ], cwd = source_dir)

        # deploy
        import shutil

        src = source_dir / "meson.pyz"
        dst_dir = self.keg / "bin"
        dst_dir.mkdir(parents=True, exist_ok=True)
        
        dst = dst_dir / "meson"
        shutil.copy2(src, dst)
        dst.chmod(
            dst.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        )
