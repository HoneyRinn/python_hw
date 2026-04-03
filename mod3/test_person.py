# tests/test_person.py
import unittest
from freezegun import freeze_time

from person import Person


class PersonTestCase(unittest.TestCase):
    def test_get_name(self):
        person = Person("Иван", 2000)
        self.assertEqual(person.get_name(), "Иван")

    def test_set_name(self):
        person = Person("Иван", 2000)
        person.set_name("Пётр")
        self.assertEqual(person.get_name(), "Пётр")

    def test_set_address(self):
        person = Person("Иван", 2000)
        person.set_address("Москва")
        self.assertEqual(person.get_address(), "Москва")

    @freeze_time("2026-04-03")
    def test_get_age(self):
        person = Person("Иван", 2000)
        self.assertEqual(person.get_age(), 26)

    def test_is_homeless_true(self):
        person = Person("Иван", 2000)
        self.assertTrue(person.is_homeless())

    def test_is_homeless_false(self):
        person = Person("Иван", 2000, "Москва")
        self.assertFalse(person.is_homeless())