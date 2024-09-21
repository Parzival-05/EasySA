import os
from pathlib import Path


def create_dirs_if_not_exist(paths: list[str | Path]):
    for path in paths:
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
