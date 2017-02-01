import os
import unittest
from app.api.helpers import convert_iso_to_json, convert_json_to_iso

class TestHelper(unittest.TestCase):
    def test_convert_iso_to_json(self):
        convert = convert_iso_to_json("2016-12-31")
        result = {'month': '12', 'year': '2016', 'day': '31'}
        self.assertEqual(convert, result)

    def test_convert_json_to_iso(self):
        convert = convert_json_to_iso({'month': '12', 'year': '2016', 'day': '31'})
        result = "2016-12-31"
        self.assertEqual(convert, result)