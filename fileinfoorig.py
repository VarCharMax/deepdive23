"""Framework for getting filetype-specific metadata.
Instantiate appropriate class with filename. Returned object acts like a
dictionary, with key-value pairs for each piece of metadata.
import fileinfo
info = fileinfo.MP3FileInfo("/music/ap/mahadeva.mp3")
print("\n".join(["%s=%s" % (k, v) for k, v in info.items()]))
Or use listdirectory function to get info on all files in a directory.
for info in fileinfo.listdirectory("/music/ap/", [".mp3"]):
...
Framework can be extended by adding classes for particular file types, e.g.
HTMLFileInfo, MPGFileInfo, DOCFileInfo. Each class is completely responsible for
parsing its files appropriately; see MP3FileInfo for example.
"""

import os
import sys


def stripnulls(data: bytes) -> bytes:
    "strip whitespace and nulls"
    return data.replace(b"\x00", b" ").strip()


class FileInfo(dict):
    """Initialize this parent class key ["name"] with filename value."""

    def __init__(self, filename=None) -> None:
        """This implementation does not override dict __init()__, which expects a k,v pair.
        We just redefine the init here for our own purposes."""
        self["name"] = filename


class MP3FileInfo(FileInfo):
    "store ID3v1.0 MP3 tags"

    tagDataMap = {
        "title": (3, 33, stripnulls),
        "artist": (33, 63, stripnulls),
        "album": (63, 93, stripnulls),
        "year": (93, 97, stripnulls),
        "comment": (97, 126, stripnulls),
        "genre": (127, 128, ord),
    }

    def __parse(self, filename: str) -> None:
        "parse ID3v1.0 tags from MP3 file"
        self.clear()
        try:
            with open(filename, "rb", 0) as fsock:
                fsock.seek(-128, 2)
                tagdata = fsock.read(128)

                if tagdata[:3].decode() == "TAG":
                    # Dictionary with string key, tuple value of (start, end, parsefunc).
                    for tag, (start, end, parsefunc) in self.tagDataMap.items():
                        # Call back to __setitem__ to add key-value pair to dictionary.
                        self[tag] = parsefunc(tagdata[start:end].decode())  # utf-8
        except IOError:
            pass

    def __setitem__(self, key: str, item: str) -> None:
        """Called after parent dictionary is initialised with first key ["name"].
            Then goes on to parse additional metadata.
        Args:
            key (_type_): _description_
            item (_type_): _description_
        """
        if key == "name" and item:
            self.__parse(item)
        FileInfo.__setitem__(self, key, item)


def listdirectory(directory, fileextlist) -> list[FileInfo]:
    "get list of dictionaries containing meta info for files of specified extension"
    # Get list of files in directory.
    filelist = [os.path.normcase(f) for f in os.listdir(directory)]
    # Create full path to file, filter by extension.
    filelist = [
        os.path.join(directory, f)
        for f in filelist
        if os.path.splitext(f)[1] in fileextlist
    ]

    def getfileinfoclass(
        filename, module=sys.modules[FileInfo.__module__]
    ) -> type[FileInfo]:
        "get file info class according to filename extension"
        subclass = f"{os.path.splitext(filename)[1].upper()[1:]}FileInfo"
        return hasattr(module, subclass) and getattr(module, subclass) or FileInfo

    # Get custom dictionary object for specific file type,
    # Initialise parent dictionary with ["name"]=<filename>,
    # Parse file meta data into child dictionary and return list of dictionaries.
    return [getfileinfoclass(f)(f) for f in filelist]


if __name__ == "__main__":
    # info is subclassed FileInfo dictionary containing file metadata.
    for info in listdirectory("/Users/rohanparkes/tmp/", [".mp3"]):
        print("\n".join([f"{k}={v}" for (k, v) in info.items()]))
        print()
