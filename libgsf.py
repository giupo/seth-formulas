from seth.formula import Formula


class LibgsfFormula(Formula):
    """libgsf: structured file (OLE2/MS-DOC) library, required by libpst's
    `readpst` to read attachments. Its autotools build hard-requires
    intltool regardless of --disable-nls, and requires glib/gobject/gio
    >= 2.62 (see [[intltool]] and [[glib]])."""

    name = "libgsf"
    latest = "1.14.58"
    dependencies = ["glib", "libxml2", "zlib"]
    build_dependencies = ["intltool"]

    versions = {
        "1.14.58": {
            "url": "https://download.gnome.org/sources/libgsf/1.14/libgsf-1.14.58.tar.xz",
            "sha256": "06e07ea12b7a52b9e316faddfecb640b1717a4875c59f0efb3b0cec1e2ccf35a",
        },
    }

    def configure_args(self):
        return [
            f"--prefix={self.keg}",
            "--disable-gtk-doc",
            "--disable-introspection",
            "--without-gdk-pixbuf",
            "--without-bz2",
        ]
