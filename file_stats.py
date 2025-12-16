"""_summary_

Raises:
    ValueError: _description_

Returns:
    _type_: _description_
"""

from datetime import datetime
import os
import sys
import glob


def secondstotime(time_in_seconds) -> str:
    """_summary_

    Returns:
        str: _description_
    """
    return datetime.fromtimestamp(time_in_seconds).strftime("%d/%m/%Y %I:%M:%S %p")


def get_human_readable_size(size_bytes) -> str:
    """
    Convert a file size from bytes to a human-readable string (B, KB, MB, GB, TB).
    """
    if size_bytes == 0:
        return "0 Bytes"

    # Define the units and their divisor (1024 for KiB, MiB, etc.)
    units = ["Bytes", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(units) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.2f} {units[i]}"


def check_attributes(attrs: int) -> str:
    """_summary_

    Args:
        filepath (_type_): _description_
    """

    # pylint: disable=import-outside-toplevel
    if sys.platform == "win32":
        import win32con

        attribs = set()

        try:
            # Check for common attributes using bitwise AND and win32con constants
            # If (attrs & CONSTANT) is non-zero, the attribute is set.

            if attrs & win32con.FILE_ATTRIBUTE_READONLY:
                attribs.add("Read-Only")
            if attrs & win32con.FILE_ATTRIBUTE_HIDDEN:
                attribs.add("Hidden")
            if attrs & win32con.FILE_ATTRIBUTE_SYSTEM:
                attribs.add("System")
            if attrs & win32con.FILE_ATTRIBUTE_DIRECTORY:
                attribs.add("Directory")
            if attrs & win32con.FILE_ATTRIBUTE_ARCHIVE:
                attribs.add("Archive")
            if attrs & win32con.FILE_ATTRIBUTE_NORMAL:
                attribs.add("Normal")
            if attrs & win32con.FILE_ATTRIBUTE_TEMPORARY:
                attribs.add("Temporary")
            if attrs & win32con.FILE_ATTRIBUTE_COMPRESSED:
                attribs.add("Compressed")
            if attrs & win32con.FILE_ATTRIBUTE_ENCRYPTED:
                attribs.add("Encrypted")

            return ", ".join(list(attribs))

        except Exception:
            pass

    return ""


def st_to_human(key, val) -> str:
    """_summary_

    Args:
        item (_type_): _description_

    Returns:
        str: _description_
    """
    name, processfunc = dict_methods[key]

    return f"{name}: {processfunc(val)}"


def file_mode(mode) -> str:
    """_summary_

    Args:
        mode (_type_): _description_

    Returns:
        str: _description_
    """
    # pylint: disable=import-outside-toplevel
    if sys.platform == "win32":
        import stat

        return stat.filemode(mode)

    return ""


dict_methods = {
    "st_mode": ("File Mode", file_mode),
    "st_ino": ("File Index", int),
    "st_dev": ("Device Id", int),
    "st_nlink": ("Hard Link Count", int),
    "st_uid": ("User Id", int),
    "st_gid": ("Group Id", int),
    "st_size": ("Size", get_human_readable_size),
    "st_atime": ("Last Accessed", secondstotime),
    "st_mtime": ("Last Modified", secondstotime),
    "st_ctime": ("Metadata Changed", secondstotime),
    "st_birthtime": ("File Created", secondstotime),
    "st_file_attributes": ("File Attributes", check_attributes),
    "st_reparse_tag": ("Reparse Type", int),
}


def format_dict(stat_dict) -> str:
    """_summary_

    Args:
        stat_dict (_type_): _description_

    Returns:
        str: _description_
    """
    ret = "\n\t".join([st_to_human(k, v) for (k, v) in stat_dict.items()])

    return "\t" + ret


def stats_to_dict(filestat) -> dict[str, int]:
    """
    Docstring for stat_to_dict

    :param filestat: Description
    :return: Description
    :rtype: dict[str, Any]
    """
    if not isinstance(filestat, os.stat_result):
        raise ValueError(f"argument must be os.stat_result, not {type(filestat)}")

    # Dictionary comprehension. Exclude newer nanosecond properties.
    ret = {
        attr: getattr(filestat, attr)
        for attr in dir(filestat)
        if attr.startswith("st_") and not attr.endswith("_ns")
    }

    return ret


if __name__ == "__main__":
    metadata_dict = {
        f: format_dict(stats_to_dict(os.stat(f))) for f in glob.glob("fib.py")
    }
    print("".join([f"{k}:\n{v}" for (k, v) in metadata_dict.items()]))
