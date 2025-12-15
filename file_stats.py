"""_summary_

Raises:
    ValueError: _description_

Returns:
    _type_: _description_
"""

import os
import glob
from typing import Any


def stat_to_dict(filestat) -> dict[str, Any]:
    """
    Docstring for stat_to_dict

    :param filestat: Description
    :return: Description
    :rtype: dict[str, Any]
    """
    if not isinstance(filestat, os.stat_result):
        raise ValueError(f"argument must be os.stat_result, not {type(filestat)}")

    return {
        attr: getattr(filestat, attr)
        for attr in dir(filestat)
        if attr.startswith("st_")
    }


if __name__ == "__main__":
    metadata_dict = {f: stat_to_dict(os.stat(f)) for f in glob.glob("*info*.py")}
    print(metadata_dict)
