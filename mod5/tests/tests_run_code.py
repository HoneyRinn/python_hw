import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app


class RunCodeTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        cls.client = app.test_client()

    def test_valid_code(self):
        response = self.client.post(
            "/run_code",
            data={"code": "print('Hello world')", "timeout": 2},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello world", response.data.decode())

    def test_timeout(self):
        response = self.client.post(
            "/run_code",
            data={
                "code": "import time\ntime.sleep(2)\nprint('done')",
                "timeout": 1,
            },
        )
        self.assertEqual(response.status_code, 408)
        self.assertIn("Время выполнения кода истекло", response.data.decode())

    def test_invalid_timeout(self):
        response = self.client.post(
            "/run_code",
            data={"code": "print('ok')", "timeout": 31},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("timeout", response.get_json()["errors"])

    def test_missing_code(self):
        response = self.client.post(
            "/run_code",
            data={"timeout": 2},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("code", response.get_json()["errors"])

    def test_shell_injection_not_executed(self):
        code = 'print("ok"); system("echo hacked")' 
        response = self.client.post(
            "/run_code",
            data={"code": code, "timeout": 2},
        )
        text = response.data.decode()
        self.assertNotIn("\nhacked\n", text) 
        self.assertIn("NameError", text)


if __name__ == "__main__":
    unittest.main()