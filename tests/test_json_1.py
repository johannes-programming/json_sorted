import json
import tempfile
import unittest
from io import BufferedReader, BufferedWriter
from pathlib import Path
from typing import Any, Self

from normdata.enum.Instruction import Instruction
from normdata.json.run import run

__all__ = ["TestRun"]


def get_instruction(reverse: bool) -> Instruction:
    instruction: Instruction
    for instruction in Instruction:
        if instruction.value == reverse:
            return instruction
    raise AssertionError(f"No Instruction found with value={reverse!r}")


def write_json(path: Path, data: dict[str, Any]) -> None:
    stream: Any
    with path.open("w") as stream:
        json.dump(data, stream)


def read_json(path: Path) -> Any:
    stream: Any
    with path.open("r") as stream:
        return json.load(stream)


class TestRun(unittest.TestCase):
    def test_run_sorts_root_table_ascending(self: Self) -> None:
        asc: Instruction
        data: dict[str, Any]
        path: Path
        tmpdir: str
        asc = get_instruction(False)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "example.json"
            write_json(path, {"z": 1, "a": 2, "m": 3})
            run(str(path), instructions=[asc])
            data = read_json(path)
            self.assertEqual(list(data.keys()), ["a", "m", "z"])

    def test_run_sorts_root_table_descending(self: Self) -> None:
        data: dict[str, Any]
        desc: Instruction
        path: Path
        tmpdir: str
        desc = get_instruction(True)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "example.json"
            write_json(path, {"a": 1, "z": 2, "m": 3})
            run(str(path), instructions=[desc])
            data = read_json(path)
            self.assertEqual(list(data.keys()), ["z", "m", "a"])

    def test_run_sorts_nested_table_by_key_path(self: Self) -> None:
        asc: Instruction
        data: dict[str, Any]
        nested: Any
        path: Path
        tmpdir: str
        asc = get_instruction(False)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "example.json"
            write_json(
                path,
                {
                    "tool": {
                        "fooooooo": {
                            "z": 1,
                            "a": 2,
                            "m": 3,
                        }
                    }
                },
            )
            run(
                str(path),
                instructions=[asc, "tool", "fooooooo"],
            )
            data = read_json(path)
            nested = data["tool"]["fooooooo"]
            self.assertEqual(list(nested.keys()), ["a", "m", "z"])

    def test_run_sorts_nested_list_by_key_path(self: Self) -> None:
        asc: Any
        data: dict[str, Any]
        path: Path
        tmpdir: str
        asc = get_instruction(False)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "example.json"
            write_json(path, {"project": {"numbers": [3, 1, 2]}})
            run(
                str(path),
                instructions=[asc, "project", "numbers"],
            )
            data = read_json(path)
            self.assertEqual(data["project"]["numbers"], [1, 2, 3])

    def test_run_accepts_glob_patterns(self: Self) -> None:
        asc: Instruction
        first: Path
        root: Path
        second: Path
        tmpdir: str
        asc = get_instruction(False)
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            first = root / "first.json"
            second = root / "second.json"
            write_json(first, {"b": 1, "a": 2})
            write_json(second, {"d": 1, "c": 2})
            run(str(root / "*.json"), instructions=[asc])
            self.assertEqual(list(read_json(first).keys()), ["a", "b"])
            self.assertEqual(list(read_json(second).keys()), ["c", "d"])

    def test_run_ignores_duplicate_file_matches(self: Self) -> None:
        asc: Instruction
        data: dict[str, Any]
        path: Path
        tmpdir: str
        asc = get_instruction(False)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "example.json"
            write_json(path, {"b": 1, "a": 2})
            run(str(path), str(path), instructions=[asc])
            data = read_json(path)
            self.assertEqual(list(data.keys()), ["a", "b"])

    def test_run_raises_type_error_for_unsortable_value(self: Self) -> None:
        asc: Instruction
        path: Path
        tmpdir: str
        asc = get_instruction(False)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "example.json"
            write_json(path, {"project": {"name": "demo"}})
            with self.assertRaises(TypeError):
                run(
                    str(path),
                    instructions=[asc, "project", "name"],
                )


if __name__ == "__main__":
    unittest.main()
