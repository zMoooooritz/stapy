import unittest
from unittest import mock

from stapy.cli.parser import Parser
from stapy.sta.entity import Entity
from stapy.common.config import config

class Args(object):

    def __init__(self, add=None, patch=None, delete=None, getr=None, url=None):
        self.add = add
        self.patch = patch
        self.delete = delete
        self.getr = getr
        self.url = url
        self.inter = None

class TestParserMethods(unittest.TestCase):

    def setUp(self):
        self.parser = Parser(construct=False)

    def test_url(self):
        config.set(api_url="")
        args = Args(add=[""])
        self.assertEqual(self.parser.parse_args(args), -1)
        args = Args(url=["value"])
        self.parser.parse_args(args)
        self.assertEqual(config.get("api_url"), "value/")

    @mock.patch('stapy.sta.post.Post.entity')
    def test_add(self, mocked_post):
        args = Args(add=["help"])
        self.assertEqual(self.parser.parse_args(args), 1)
        args = Args(add=["xyz"])
        self.assertEqual(self.parser.parse_args(args), 3)
        args = Args(add=["ObservedProperty"])
        self.assertEqual(self.parser.parse_args(args), 2)

        data = {"name": "Testing", "description": "in", "definition": "Production"}
        args = Args(add=["ObservedProperty"] + [*data.values()])
        ret = self.parser.parse_args(args)
        params, kparams = mocked_post.call_args
        self.assertEqual(ret, 0)
        self.assertEqual(params[0], Entity.ObservedProperty)
        self.assertEqual(kparams, data)

    @mock.patch('stapy.sta.patch.Patch.entity')
    def test_patch(self, mocked_patch):
        args = Args(patch=["help"])
        self.assertEqual(self.parser.parse_args(args), 1)
        args = Args(patch=["xyz"])
        self.assertEqual(self.parser.parse_args(args), 3)
        args = Args(patch=["ObservedProperty"])
        self.assertEqual(self.parser.parse_args(args), 2)
        args = Args(patch=["ObservedProperty", 7])
        self.assertEqual(self.parser.parse_args(args), 2)

        data = {"name": "Testing", "description": "in", "definition": "Production"}
        args = Args(patch=["ObservedProperty", 7, "name=Testing", "properties={\"test\": 15}"])
        ret = self.parser.parse_args(args)
        params, kparams = mocked_patch.call_args
        self.assertEqual(ret, 0)
        self.assertEqual(params[0], Entity.ObservedProperty)
        self.assertEqual(params[1], 7)
        self.assertEqual(kparams, {"name": "Testing", "properties": "{\"test\": 15}"})

    @mock.patch('stapy.sta.delete.Delete.query')
    @mock.patch('stapy.sta.delete.Delete.entity')
    def test_delete(self, mocked_delete_e, mocked_delete_q):
        args = Args(delete=["help"])
        self.assertEqual(self.parser.parse_args(args), 1)
        args = Args(delete=["xyz"])
        self.assertEqual(self.parser.parse_args(args), 3)
        args = Args(delete=["ObservedProperty"])
        self.assertEqual(self.parser.parse_args(args), 2)

        ids = [1, 15, 99]
        args = Args(delete=["ObservedProperty"] + ids)
        ret = self.parser.parse_args(args)
        params, kparams = mocked_delete_e.call_args
        self.assertEqual(ret, 0)
        self.assertEqual(params[0], Entity.ObservedProperty)
        self.assertEqual(params[1:][0], ids)

        path = "/Datastream(1)/ObservedProperties"
        args = Args(delete=["ObservedProperty", path])
        ret = self.parser.parse_args(args)
        params, kparams = mocked_delete_q.call_args
        self.assertEqual(ret, 0)
        self.assertEqual(params[0], path)

    def test_getr(self):
        args = Args(getr=[""])
        self.assertEqual(self.parser.parse_args(args), -1)


if __name__ == '__main__':
    unittest.main()
