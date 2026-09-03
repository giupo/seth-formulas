from seth.formula import Formula


class LibpstFormula(Formula):
    """libpst: provides the `readpst` CLI that ostpst shells out to as a
    fallback when its native Go .pst/.ost parser (go-pst) can't handle a
    file - e.g. the "4k page format" used by some large/newer .ost files,
    which go-pst mishandles (see internal/readpst in the ostpst repo)."""

    name = "libpst"
    latest = "0.6.76"
    dependencies = ["libgsf", "glib"]

    versions = {
        "0.6.76": {
            "url": "https://www.five-ten-sg.com/libpst/packages/libpst-0.6.76.tar.gz",
            "sha256": "3d291beebbdb48d2b934608bc06195b641da63d2a8f5e0d386f2e9d6d05a0b42",
        },
    }

    def configure_args(self):
        return [
            f"--prefix={self.keg}",
            "--disable-python",
            # readpst.c has an old K&R-style forward declaration
            # (`int grim_reaper();`) that GCC 14+'s C23 default treats as a
            # hard "conflicting types" error against its full-prototype
            # definition; -std=gnu17 restores pre-C23 semantics.
            "CFLAGS=-std=gnu17",
        ]
