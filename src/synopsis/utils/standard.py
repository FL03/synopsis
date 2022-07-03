import os
import datetime
from pydantic import BaseModel
from typing import List


def file_suffix(filepath: str) -> str:
    return os.path.splitext(filepath)[-1].strip(".")


def merge_dicts(a: dict, b: dict) -> dict:
    return dict(a, **b)


def convert_lom_to_lod(*args: BaseModel) -> List[dict]:
    return [i.dict() for i in args]


def indexer(*args):
    return [i for i, j in enumerate(args)]


def timestamp() -> str: return str(datetime.datetime.now())
