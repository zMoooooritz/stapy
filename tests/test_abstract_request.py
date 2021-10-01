import unittest
from unittest import mock

from stapy.sta.post import Post
from stapy.sta.entity import Entity
from stapy.sta.request import Request
import stapy.sta.entities as ent

class PostMock(object):
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
        self.ok = status_code < 400
        self.headers = {"location": "(1)"}

    def json(self):
        return self.json_data


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

    @mock.patch("requests.post")
    def test_send_request(self, mocked_post):
        mocked_post.side_effect = Exception()
        with self.assertRaises(ValueError):
            Post.send_request(Request.POST, "", "")
        mocked_post.side_effect = None
        mocked_post.return_value = PostMock({"message": "test"}, 404)
        self.assertEqual(Post.send_request(Request.POST, "", ""), -1)
        mocked_post.return_value = PostMock({}, 404)
        self.assertEqual(Post.send_request(Request.POST, "", ""), -1)
        with self.assertRaises(Exception):
            Post.send_request(Request.DELETE, "", "")


if __name__ == "__main__":
    unittest.main()
