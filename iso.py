"""
Detect file size from ISO file or stream.
"""

# pylint: disable=superfluous-parens,line-too-long
import os
import sys
from cStringIO import StringIO
from isoparser.iso import ISO
from isoparser.source import Source, SECTOR_LENGTH
from isoparser.volume_descriptors import PrimaryVD

class StreamSource(Source):
    """
    ISO parser stream source
    """

    def __init__(self, iso_file, **kwargs):
        super(StreamSource, self).__init__(**kwargs)
        self._buf = StringIO()
        self._buf_length = 0
        self._file = iso_file

    def read_until(self, pos):
        """
        Read to the start of the byte offset `pos` and return the contents.
        """

        oldpos = self._buf.tell()
        if pos <= oldpos:
            return ""

        contents = self._buf.read(min(self._buf_length, pos) - oldpos)
        if self._buf_length < pos:
            new_contents = self._file.read(pos - self._buf_length)
            self._buf.seek(0, os.SEEK_END)
            self._buf.write(new_contents)
            self._buf_length = pos

            contents += new_contents

        return contents

    def seek_to(self, pos):
        """
        Seek to the byte offset `pos`.
        """

        self.read_until(pos)
        self._buf.seek(pos)

    def _read_for(self, length):
        return self.read_until(self._buf.tell() + length)

    def _fetch(self, sector, count=1):
        self.seek_to(sector * SECTOR_LENGTH)
        return self._read_for(SECTOR_LENGTH * count)

def main():
    """
    Main entry point.
    """

    path = sys.argv[1] if len(sys.argv) > 1 else "-"
    output = sys.argv[2] if len(sys.argv) > 2 else None
    if path == "-":
        iso_file = sys.stdin
        from_stdin = True
        text = "the initial seek location of the stream"
    else:
        iso_file = open(path, "rb")
        from_stdin = False
        text = "the start of the file"

    source = StreamSource(iso_file)
    iso = ISO(source)

    size = 0
    for descriptor in iso.volume_descriptors.itervalues():
        if isinstance(descriptor, PrimaryVD):
            size += descriptor.volume_space_size * descriptor.logical_block_size

    if output is not None:
        with open(output, "wb") as extracted_file:
            source.seek_to(0)
            extracted_file.write(source.read_until(size))
    else:
        print("The first {} bytes from {} are part of the ISO image.".format(size, text))

    if not from_stdin:
        iso_file.close()

if __name__ == "__main__":
    main()
