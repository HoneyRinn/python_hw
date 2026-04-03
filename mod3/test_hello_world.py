import unittest
from freezegun import freeze_time

from app import app, get_weekday_name


class HelloWorldTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @freeze_time("2026-04-01")  # среда
    def test_get_weekday_name(self):
        self.assertEqual(get_weekday_name(), "среды")

    @freeze_time("2026-04-01")
    def test_hello_world_with_normal_name(self):
        response = self.client.get("/hello-world/Саша")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Привет, Саша. Хорошей среды!")

    @freeze_time("2026-04-01")
    def test_hello_world_with_phrase_as_name(self):
        response = self.client.get("/hello-world/Хорошей среды")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Привет, Хорошей среды. Хорошей среды!")