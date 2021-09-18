import unittest

from stapy.sta.post import Post
from stapy.sta.entity import Entity
import stapy.sta.entities as ent


class TestAbstractRequestMethods(unittest.TestCase):

    def test_get_entity(self):
        self.assertEqual(Post.get_entity(Entity.Datastream), ent.Datastream)

    def test_cast_params(self):
        self.assertEqual({"Locations": 123}, Post.cast_params(location_id=123))
        self.assertEqual({}, Post.cast_params(value=None))
        with self.assertRaises(Exception):
            Post.cast_params(10)
        with self.assertRaises(Exception):
            Post.cast_params(xyz_id=10)

if __name__ == '__main__':
    unittest.main()
