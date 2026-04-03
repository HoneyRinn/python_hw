# tests/test_finance.py
import unittest

from app import app, storage


class FinanceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def setUp(self):
        storage.clear()
        storage.setdefault(2024, {}).setdefault(3, 0)
        storage[2024][3] = 1500
        storage.setdefault(2024, {}).setdefault(4, 0)
        storage[2024][4] = 2500
        storage.setdefault(2025, {}).setdefault(1, 0)
        storage[2025][1] = 700

    def test_add_endpoint(self):
        response = self.client.get("/add/20240315/500")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Добавлено 500 рублей за 20240315", response.data.decode())

    def test_add_invalid_date_raises(self):
        with self.assertRaises(ValueError):
            with app.test_request_context():
                from app import add
                add("2024-03-15", 500)

    def test_calculate_year(self):
        response = self.client.get("/calculate/2024")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Суммарные траты за 2024: 4000")

    def test_calculate_month(self):
        response = self.client.get("/calculate/2024/3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Суммарные траты за 2024-3: 1500")

    def test_calculate_year_when_storage_empty(self):
        storage.clear()
        response = self.client.get("/calculate/2024")
        self.assertEqual(response.data.decode(), "0")

    def test_calculate_month_when_storage_empty(self):
        storage.clear()
        response = self.client.get("/calculate/2024/3")
        self.assertEqual(response.data.decode(), "0")