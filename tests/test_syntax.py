from pathlib import Path
import py_compile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SyntaxTests(unittest.TestCase):
    def test_python_files_compile(self):
        for path in ROOT.rglob("*.py"):
            if "tests" in path.parts:
                continue
            py_compile.compile(str(path), doraise=True)


if __name__ == "__main__":
    unittest.main()
