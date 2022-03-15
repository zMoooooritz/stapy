import logging
import unittest
import requests
from unittest import mock

from stapy.cli.parser import Parser
from stapy.sta.entity import Entity
from stapy.common.log import Log
from stapy.common.config import config, set_sta_url

logging.disable(logging.CRITICAL)

class Args(object):

    def __init__(self, add=None, patch=None, delete=None, getr=None, url=None, cred=None, log=None, inter=None):
        self.add = add
        self.patch = patch
        self.delete = delete
        self.getr = getr
        self.url = url
        self.cred = cred
        self.log = log
        self.inter = inter

class TestParserMethods(unittest.TestCase):

    def setUp(self):
        self.parser = Parser(construct=False)
        self.url = config.load_sta_url()
        set_sta_url("localhost:8080/FROST-Server/v1.1")

    def tearDown(self):
        set_sta_url(self.url)
    
    @mock.patch("argparse.ArgumentParser.parse_args")
    def test_construct_parser(self, mocked_args):
        mocked_args.return_value = Args(add=["help"])
        self.assertEqual(Parser().parse_args(), 1)

    @mock.patch("argparse.ArgumentParser.parse_args")
    def test_log_level(self, mocked_args):
        mocked_args.return_value = Args(log=Log.WARNING)
        self.assertEqual(Parser().get_log_level(), Log.WARNING.value)

    def test_url(self):
        config.remove("STA_URL")
        args = Args(add=[""])
        self.assertEqual(self.parser.parse_args(args), -1)
        args = Args(url=["value"])
        self.parser.parse_args(args)
        self.assertEqual(config.load_sta_url(), "value/")

    def test_url(self):
        config.remove("STA_USR")
        config.remove("STA_PWD")
        self.assertEqual(config.load_authentication(), None)
        args = Args(cred=["username", "password"])
        self.parser.parse_args(args)
        self.assertEqual(config.load_authentication(), requests.auth.HTTPBasicAuth("username", "password"))

    @mock.patch("stapy.sta.post.Post.entity")
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

        args = Args(add=["ObservedProperty"] + [*data.values()] + ["properties=7"])
        ret = self.parser.parse_args(args)
        params, kparams = mocked_post.call_args
        self.assertEqual(kparams.get("properties"), "7")
        self.assertNotIn("test", kparams.keys())

        args = Args(add=["ObservedProperty"] + [*data.values()] + ["properties7"])
        ret = self.parser.parse_args(args)
        params, kparams = mocked_post.call_args
        self.assertNotIn("properties", kparams.keys())


    @mock.patch("stapy.sta.patch.Patch.entity")
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
        args = Args(patch=["ObservedProperty", 7, "name=Testing", "properties={\"test\": 15}", "nonvalidoption"])
        ret = self.parser.parse_args(args)
        params, kparams = mocked_patch.call_args
        self.assertEqual(ret, 0)
        self.assertEqual(params[0], Entity.ObservedProperty)
        self.assertEqual(params[1], 7)
        self.assertEqual(kparams, {"name": "Testing", "properties": "{\"test\": 15}"})

    @mock.patch("stapy.sta.delete.Delete.query")
    @mock.patch("stapy.sta.delete.Delete.entity")
    def test_delete(self, mocked_delete_e, mocked_delete_q):
        args = Args(delete=["help"])
        self.assertEqual(self.parser.parse_args(args), 1)
        args = Args(delete=["xyz", 10])
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
        args = Args(delete=[path])
        ret = self.parser.parse_args(args)
        params, kparams = mocked_delete_q.call_args
        self.assertEqual(ret, 0)
        self.assertEqual(params[0], path)

    def test_getr(self):
        args = Args(getr=[""])
        self.assertEqual(self.parser.parse_args(args), -1)

    @mock.patch("stapy.cli.cli.CLI.main")
    def test_inter(self, mocked_cli):
        args = Args(inter=True)
        self.assertEqual(self.parser.parse_args(args), 0)


if __name__ == "__main__":
    unittest.main()
