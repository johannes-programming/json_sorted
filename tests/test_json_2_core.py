import json
import tempfile
import unittest
from io import BufferedReader, BufferedWriter
from pathlib import Path
from typing import Any, Self

from normdata.enum.Instruction import Instruction
from normdata.enum.Selector import Selector
from normdata.json.run import run

__all__ = ["TestAllKeys"]


def write_json(path: Path, data: dict[str, Any]) -> None:
    stream: Any
    with path.open("w") as stream:
        json.dump(data, stream)


def read_json(path: Path) -> Any:
    stream: Any
    with path.open("r") as stream:
        return json.load(stream)


class TestAllKeys(unittest.TestCase):

    def test_all_keys_expands_every_child_table(self: Self) -> None:
        data: dict[str, Any]
        path: Path
        tmpdir: str
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "example.json"
            write_json(
                path,
                {
                    "tool": {
                        "x": {"c": 1, "a": 2, "b": 3},
                        "y": {"z": 1, "m": 2},
                    }
                },
            )
            # --sort --key=tool --all-keys
            run(
                "json",
                str(path),
                instructions=[Instruction.SORT, "tool", Selector.ALL_KEYS],
            )
            data = read_json(path)
            self.assertEqual(list(data["tool"]["x"].keys()), ["a", "b", "c"])
            self.assertEqual(list(data["tool"]["y"].keys()), ["m", "z"])

    def test_all_keys_expands_list_elements(self: Self) -> None:
        data: dict[str, Any]
        path: Path
        tmpdir: str
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "example.json"
            write_json(path, {"rows": [[3, 1, 2], [9, 8, 7]]})
            # --sort --key=rows --all-keys
            with self.assertRaises(Exception):
                run(
                    "json",
                    str(path),
                    instructions=[Instruction.SORT, "rows", Selector.ALL_KEYS],
                )

    def test_all_indices_expands_list_elements(self: Self) -> None:
        data: dict[str, Any]
        path: Path
        tmpdir: str
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "example.json"
            write_json(path, {"rows": [[3, 1, 2], [9, 8, 7]]})
            # --sort --key=rows --all-indices
            run(
                "json",
                str(path),
                instructions=[Instruction.SORT, "rows", Selector.ALL_INDICES],
            )
            data = read_json(path)
            self.assertEqual(data["rows"], [[1, 2, 3], [7, 8, 9]])


if __name__ == "__main__":
    unittest.main()
