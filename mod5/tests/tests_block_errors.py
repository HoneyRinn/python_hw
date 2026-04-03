import unittest

from app import BlockErrors

class TestBlockErrors(unittest.TestCase):
    def test_ignore_error(self):
        with BlockErrors({ZeroDivisionError}):
            a = 1 / 0  # не падает

    def test_raise_unexpected_error(self):
        with self.assertRaises(TypeError):
            with BlockErrors({ZeroDivisionError}):
                a = 1 / "0"

    def test_nested_blocks(self):
        with BlockErrors({TypeError}):
            with BlockErrors({ZeroDivisionError}):
                a = 1 / "0" 

    def test_ignore_all_exceptions(self):
        with BlockErrors({Exception}):
            a = 1 / "0"


if __name__ == "__main__":
    unittest.main()