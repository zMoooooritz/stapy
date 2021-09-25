from stapy.sta.geo import GeoJSON

import unittest

class TestGeoJSONMethods(unittest.TestCase):

    def test_list(self):
        self.assertEqual(len(GeoJSON), len(GeoJSON.list()))
        self.assertIn(GeoJSON.Point.value, GeoJSON.list())

    def test_match(self):
        self.assertEqual(GeoJSON.Point, GeoJSON.match("Pont"))
        self.assertEqual(GeoJSON.MultiPolygon, GeoJSON.match("multypol"))
        self.assertIsNone(GeoJSON.match("xyz"))
        self.assertIsNone(GeoJSON.match(123))

    def test_is_valid(self):
        self.assertFalse(GeoJSON.is_valid("Point", [1, 1]))
        self.assertFalse(GeoJSON.is_valid(GeoJSON.Point, [1]))
        self.assertFalse(GeoJSON.is_valid(GeoJSON.Point, []))
        self.assertTrue(GeoJSON.is_valid(GeoJSON.Point, [0, 1]))
        with self.assertRaises(Exception):
            GeoJSON.is_valid(GeoJSON.Point, "1, 2")

if __name__ == '__main__':
    unittest.main()
