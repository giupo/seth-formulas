from seth.formula import Formula


class ImagemagickFormula(Formula):
    name = "imagemagick"
    latest = "7.1.2-25"
    dependencies = ["zlib"]
    build_dependencies = ["pkgconfig"]

    versions = {
        "7.1.2-25": {
            "url": "https://github.com/ImageMagick/ImageMagick/archive/refs/tags/7.1.2-25.tar.gz",
            "sha256": "ff33d227d2e1744327280e956ec9f7abaebbd8f48277d16cdad906e05e4794b6"
        },
    }

    def configure_args(self):
        return [
            f"--prefix={self.keg}",
            "--enable-shared",
            "--disable-static",
            "--without-x",          # no X11 — headless/server build
            "--with-zlib=yes",
            "--without-bzlib",      # skip bzip2 unless formula added
            "--without-lzma",
            "--without-png",        # skip unless libpng formula added
            "--without-jpeg",       # skip unless libjpeg formula added
            "--without-tiff",
            "--without-freetype",
            "--without-openmp",
            "--disable-docs",
        ]
