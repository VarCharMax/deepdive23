"""_summary_

Raises:
    ValueError: _description_

Returns:
    _type_: _description_
"""

import os
import glob


def format_dict(stat_dict) -> str:

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

    ret = {
        attr: getattr(filestat, attr)
        for attr in dir(filestat)
        if attr.startswith("st_")
    }

    return ret


if __name__ == "__main__":
    metadata_dict = {
        f: format_dict(stat_to_dict(os.stat(f))) for f in glob.glob("fib.py")
    }
    print("".join([f"{k}:\n{v}" for (k, v) in metadata_dict.items()]))
