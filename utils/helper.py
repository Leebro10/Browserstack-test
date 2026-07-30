import json
from pathlib import Path


def save_json(data, filepath: Path):

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )