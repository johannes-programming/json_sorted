import json
import tempfile
import unittest
from io import BufferedReader, BufferedWriter
from pathlib import Path
from typing import Any, Self

from normdata.enum.Instruction import Instruction
from normdata.enum.Selector import Selector
from normdata.json.run import run, run_instruction_on_data

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
    def test_all_keys_documented_example(self: Self) -> None:
        # --sort --key=foo --all-keys --index=0
        data: dict[str, Any]
        result: dict[str, Any]
        data = {
            "foo": {
                "bar": [[4, 2], {}],
                "baz": [{"a": 9, "c": 8, "b": 7}],
            }
        }
        result = run_instruction_on_data(
            instruction=Instruction.SORT,
            keys=["foo", Selector.ALL_KEYS, 0],
            data=data,
        )
        self.assertEqual(
            result,
            {
                "foo": {
                    "bar": [[2, 4], {}],
                    "baz": [{"a": 9, "b": 7, "c": 8}],
                }
            },
        )

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
                str(path),
                instructions=[Instruction.SORT, "rows", Selector.ALL_INDICES],
            )
            data = read_json(path)
            self.assertEqual(data["rows"], [[1, 2, 3], [7, 8, 9]])

    def test_all_keys_respects_sort_reverse(self: Self) -> None:
        data: dict[str, Any]
        result: dict[str, Any]
        data = {"foo": {"a": [3, 1, 2], "b": [6, 5, 4]}}
        result = run_instruction_on_data(
            instruction=Instruction.SORT_REVERSE,
            keys=["foo", Selector.ALL_KEYS],
            data=data,
        )
        self.assertEqual(result, {"foo": {"a": [3, 2, 1], "b": [6, 5, 4]}})

    def test_all_keys_on_scalar_raises_type_error(self: Self) -> None:
        with self.assertRaises(TypeError):
            run_instruction_on_data(
                instruction=Instruction.SORT,
                keys=[Selector.ALL_KEYS],
                data={"name": "demo"}["name"],  # type: ignore[arg-type]
            )


if __name__ == "__main__":
    unittest.main()
