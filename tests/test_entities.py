import unittest

import stapy.sta.entities as ent
from stapy.sta.geo import GeoJSON

class TestEntitiesMethods(unittest.TestCase):

    def setUp(self):
        pass

    def test_location(self):
        loc = ent.location.Location()
        self.assertTrue(loc.check_entry("location", {"type": GeoJSON.Point, "coordinates": [1, 2, 3]}))
        self.assertTrue(loc.check_entry("location", {"type": "Point", "coordinates": [1, 2, 3]}))
        self.assertFalse(loc.check_entry("location", {"type": "Point", "coordinates": []}))
        self.assertFalse(loc.check_entry("location", {"type": GeoJSON.Point, "coordinates": []}))

if __name__ == '__main__':
    unittest.main()
