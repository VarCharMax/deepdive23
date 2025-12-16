"""_summary_

Raises:
    ValueError: _description_

Returns:
    _type_: _description_
"""

import os
import glob
import time


def secondstotime() -> str:
    """_summary_

    Returns:
        str: _description_
    """
    tm = time.localtime()
    return f"{tm.tm_yday}/{tm.tm_mon}/{tm.tm_year} {tm.tm_hour}:{tm.tm_min}:{tm.tm_sec}"


def formatbytes(byte_count) -> str:
    return ""


dict_methods = {
    "st_mode": ("File Mode", ord),
    "st_ino": ("File Index", ord),
    "st_dev": ("Device Id", ord),
    "st_nlink": ("Hard Link Count", ord),
    "st_uid": ("User Id", ord),
    "st_gid": ("Group Id", ord),
    "st_size": ("Size", formatbytes),
    "st_atime": ("Lst Accessed", secondstotime),
    "st_mtime": ("Last Modified", secondstotime),
    "st_ctime": ("Metadata Changed", secondstotime),
    "st_birthtime": ("File Created", secondstotime),
}


def format_dict(stat_dict) -> str:
    """_summary_

    Args:
        stat_dict (_type_): _description_

    Returns:
        str: _description_
    """
    ret = "\n\t".join([f"{k}={v}" for (k, v) in stat_dict.items()])

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
