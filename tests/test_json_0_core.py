import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, Self

from normdata.core.run import run
from normdata.enum.Instruction import Instruction

__all__ = ["TestJsonSort"]


class TestJsonSort(unittest.TestCase):

    def test_run_sorts_matching_json_file(self: Self) -> None:
        path: Path
        tmpdir: str
        stream: Any
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "example.json"

            with path.open("w") as stream:
                json.dump({"b": 2, "a": 1}, stream)

            run(
                "json",
                str(path),
                instructions=[Instruction.SORT],
            )

            with path.open("r") as stream:
                result = json.load(stream)

        self.assertEqual(result, {"a": 1, "b": 2})

    def test_run_ignores_duplicate_glob_matches(self: Self) -> None:
        path: Path
        stream: Any
        tmpdir: str
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "example.json"

            with path.open("w") as stream:
                json.dump({"b": 2, "a": 1}, stream)

            run(
                "json",
                str(path),
                str(path),
                instructions=[Instruction.SORT],
            )

            with path.open("r") as stream:
                result = json.load(stream)

        self.assertEqual(result, {"a": 1, "b": 2})


if __name__ == "__main__":
    unittest.main()
