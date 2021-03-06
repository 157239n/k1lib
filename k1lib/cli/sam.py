# AUTOGENERATED FILE! PLEASE DON'T EDIT
"""
This is for functions that are .sam or .bam related
"""
from k1lib import cli; import k1lib
__all__ = ["cat", "header", "flag"]
settings = k1lib.Settings()
k1lib.settings.cli.add("sam", settings, "from k1lib.cli.sam module");
catF = lambda header: cli.applyS(lambda bamFile: None | cli.cmd(f"samtools view {'-h' if header else ''} {bamFile}") | cli.table("\t"))
def cat(bamFile:str=None, header:bool=True):
    """Get sam file outputs from bam file.
Example::

    sam.cat("file.bam") | display()
    "file.bam" | sam.cat(header=False) | display()

:param header: whether to include headers or not"""
    return catF(header)(bamFile) if bamFile is not None else catF(header)
settings.add("header", k1lib.Settings()
             .add("short", ["qname", "flag", "rname", "pos", "mapq", "cigar", "rnext", "pnext", "tlen", "seq", "qual"])
             .add("long", ["Query template name", "Flags", "Reference sequence name", "Position", "Mapping quality", "CIGAR string", "Rname of next read", "Position of next read", "Template length", "Sequence", "Quality"]), "sam headers")
class header(cli.BaseCli):
    def __init__(self, long=True):
        """Adds a header to the table.
Example::

    sam.cat("file.bam") | sam.header() | display()

You can change the header labels like this::

    settings.cli.sam.header.long = ["Query template name", ...]

:param long: whether to use a long descriptive header, or a short one"""
        super().__init__(); self.long = long
    def __ror__(self, it):
        return it | ~cli.insert(*(settings.header.long if self.long else settings.header.short))
settings.add("flags", ['PAIRED', 'PROPER_PAIR', 'UNMAP', 'MUNMAP', 'REVERSE', 'MREVERSE', 'READ1', 'READ2', 'SECONDARY', 'QCFAIL', 'DUP', 'SUPPLEMENTARY'], "list of flags")
class flag(cli.bindec):
    def __init__(self, f=None):
        """Decodes flags attribute.
Example::

    # returns ['PAIRED', 'UNMAP']
    5 | flag()
    # returns 'PAIRED, UNMAP'
    5 | flag(cli.join(", "))

You'll mostly use this in this format::

    sam.cat("file.bam", False) | apply(sam.flag(), 1) | display()

You can change the flag labels like this::

    settings.cli.sam.flags = ["paired", ...]

:param f: transform function fed into :class:`~k1lib.cli.utils.bindec`, defaulted
    to `join(", ")`"""
        super().__init__(k1lib.settings.cli.sam.flags, f or cli.join(", "))