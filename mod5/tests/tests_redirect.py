import unittest
import io

from app import Redirect


class TestRedirect(unittest.TestCase):
    def test_stdout_redirect(self):
        fake_out = io.StringIO()

        with Redirect(stdout=fake_out):
            print("hello")

        self.assertIn("hello", fake_out.getvalue())

    def test_stderr_redirect(self):
        fake_err = io.StringIO()

        try:
            with Redirect(stderr=fake_err):
                raise Exception("error text")
        except Exception:
            pass

        self.assertIn("error text", fake_err.getvalue())

    def test_both_streams(self):
        fake_out = io.StringIO()
        fake_err = io.StringIO()

        try:
            with Redirect(stdout=fake_out, stderr=fake_err):
                print("hello")
                raise Exception("fail")
        except Exception:
            pass

        self.assertIn("hello", fake_out.getvalue())
        self.assertIn("fail", fake_err.getvalue())

    def test_no_args(self):
        with Redirect():
            print("ok")


if __name__ == "__main__":
    unittest.main()