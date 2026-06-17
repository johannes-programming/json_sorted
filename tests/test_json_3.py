import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, Self

from normdata.json.main import main

__all__ = ["TestCliAllIndices"]


class TestCliAllIndices(unittest.TestCase):
    def test_cli_accepts_all_indices_selector(self: Self) -> None:
        data: dict[str, Any]
        dataA: dict[str, Any]
        listA: list[str]
        path: Path
        stream: Any
        tmpdir: str
        dataA = {
            "items": [
                {"b": 2, "a": 1},
                {"d": 4, "c": 3},
            ]
        }
        listA = [
            "--sort",
            "--key",
            "items",
            "--all-indices",
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "example.json"
            with path.open("w") as stream:
                json.dump(dataA, stream)
            main(listA + [str(path)])
            with path.open("r") as stream:
                data = json.load(stream)
        self.assertEqual(list(data["items"][0].keys()), ["a", "b"])
        self.assertEqual(list(data["items"][1].keys()), ["c", "d"])


if __name__ == "__main__":
    unittest.main()
