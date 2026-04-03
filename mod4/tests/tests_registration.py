import os
import sys
import unittest

# чтобы импорт app.py работал, если тесты лежат в папке test/
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app


class RegistrationTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        cls.client = app.test_client()

    def test_valid_registration(self):
        data = {
            "email": "test@example.com",
            "phone": 9123456789,
            "name": "Илья",
            "address": "Москва",
            "index": 123456,
            "comment": "Привет",
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "OK")

    def test_email_invalid(self):
        data = {
            "email": "not-an-email",
            "phone": 9123456789,
            "name": "Илья",
            "address": "Москва",
            "index": 123456,
            "comment": "Привет",
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 400)
        errors = response.get_json()["errors"]
        self.assertIn("email", errors)

    def test_email_missing(self):
        data = {
            "phone": 9123456789,
            "name": "Илья",
            "address": "Москва",
            "index": 123456,
            "comment": "Привет",
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 400)
        errors = response.get_json()["errors"]
        self.assertIn("email", errors)

    def test_phone_valid(self):
        data = {
            "email": "test@example.com",
            "phone": 9123456789,
            "name": "Илья",
            "address": "Москва",
            "index": 123456,
            "comment": "Привет",
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 200)

    def test_phone_too_short(self):
        data = {
            "email": "test@example.com",
            "phone": 12345,
            "name": "Илья",
            "address": "Москва",
            "index": 123456,
            "comment": "Привет",
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 400)
        errors = response.get_json()["errors"]
        self.assertIn("phone", errors)

    def test_phone_negative(self):
        data = {
            "email": "test@example.com",
            "phone": -9123456789,
            "name": "Илья",
            "address": "Москва",
            "index": 123456,
            "comment": "Привет",
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 400)
        errors = response.get_json()["errors"]
        self.assertIn("phone", errors)

    def test_name_missing(self):
        data = {
            "email": "test@example.com",
            "phone": 9123456789,
            "address": "Москва",
            "index": 123456,
            "comment": "Привет",
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 400)
        errors = response.get_json()["errors"]
        self.assertIn("name", errors)

    def test_address_missing(self):
        data = {
            "email": "test@example.com",
            "phone": 9123456789,
            "name": "Илья",
            "index": 123456,
            "comment": "Привет",
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 400)
        errors = response.get_json()["errors"]
        self.assertIn("address", errors)

    def test_index_valid(self):
        data = {
            "email": "test@example.com",
            "phone": 9123456789,
            "name": "Илья",
            "address": "Москва",
            "index": 123456,
            "comment": "Привет",
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 200)

    def test_index_not_a_number(self):
        data = {
            "email": "test@example.com",
            "phone": 9123456789,
            "name": "Илья",
            "address": "Москва",
            "index": "abc",
            "comment": "Привет",
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 400)

    def test_comment_optional(self):
        data = {
            "email": "test@example.com",
            "phone": 9123456789,
            "name": "Илья",
            "address": "Москва",
            "index": 123456,
        }
        response = self.client.post("/registration", data=data)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()