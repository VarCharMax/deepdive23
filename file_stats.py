"""_summary_

Raises:
    ValueError: _description_

Returns:
    _type_: _description_
"""

from datetime import datetime, timezone
import os
import glob


def secondstotime(time_in_seconds) -> str:
    """_summary_

    Returns:
        str: _description_
    """
    tm = datetime.fromtimestamp(time_in_seconds, timezone.utc)

    return f"{tm.day}/{tm.month}/{tm.year} {tm.hour}:{tm.minute}:{tm.second}"


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


dict_methods = {
    "st_mode": ("File Mode", ord),
    "st_ino": ("File Index", ord),
    "st_dev": ("Device Id", ord),
    "st_nlink": ("Hard Link Count", ord),
    "st_uid": ("User Id", ord),
    "st_gid": ("Group Id", ord),
    "st_size": ("Size", get_human_readable_size),
    "st_atime": ("Last Accessed", secondstotime),
    "st_mtime": ("Last Modified", secondstotime),
    "st_ctime": ("Metadata Changed", secondstotime),
    "st_birthtime": ("File Created", secondstotime),
    "st_file_attributes": ("File Attributes", ord),
    "st_reparse_tag": ("Reparse Type", ord),
}


def st_to_human(key, val) -> str:
    """_summary_

    Args:
        item (_type_): _description_

    Returns:
        str: _description_
    """
    name, processfunc = dict_methods[key]

    return f"{name}: {processfunc(val)}"


def format_dict(stat_dict) -> str:
    """_summary_

    Args:
        stat_dict (_type_): _description_

    Returns:
        str: _description_
    """
    ret = "\n\t".join([st_to_human(k, v) for (k, v) in stat_dict.items()])

    return "\t" + ret


def stat_to_dict(filestat) -> dict[str, int]:
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
        f: format_dict(stat_to_dict(os.stat(f))) for f in glob.glob("fib.py")
    }
    print("".join([f"{k}:\n{v}" for (k, v) in metadata_dict.items()]))
