import unittest
from unittest import mock

from stapy.sta.entity import Entity
from stapy.cli.cli import CLI, cap_first, cprompt

class TestSTAMethods(unittest.TestCase):

    @mock.patch("stapy.sta.post.Post.entity")
    @mock.patch("stapy.cli.cli.cprompt")
    def test_post_request(self, mocked_prompt, mocked_post):
        data = {"name": "TestName", "description": "TestDesc", "definition": "TestDef"}
        mocked_prompt.side_effect = ["POST", "ObservedProperty", data, False, False]
        CLI()
        params, kparams = mocked_post.call_args
        self.assertEqual(params[0], Entity.ObservedProperty)
        self.assertEqual(kparams, data)

        data = {"name": "TestName", "description": "TestDesc", "definition": "TestDef"}
        mocked_prompt.side_effect = ["POST", "ObservedProperty", data, True, {"properties": "test"}, False]
        CLI()
        params, kparams = mocked_post.call_args
        self.assertEqual(params[0], Entity.ObservedProperty)
        self.assertEqual(kparams["properties"], "test")

    @mock.patch("stapy.sta.patch.Patch.entity")
    @mock.patch("stapy.cli.cli.cprompt")
    def test_patch_request(self, mocked_prompt, mocked_patch):
        data = {"name": "TestName", "description": "", "definition": "TestDef"}
        mocked_prompt.side_effect = ["PATCH", "ObservedProperty", 42, data, False, False]
        CLI()
        params, kparams = mocked_patch.call_args
        self.assertEqual(params[0], Entity.ObservedProperty)
        self.assertEqual(params[1], 42)
        self.assertEqual(kparams["name"], data["name"])
        self.assertEqual(kparams["definition"], data["definition"])
        self.assertNotIn("description", kparams)

    @mock.patch("stapy.sta.delete.Delete.entity")
    @mock.patch("stapy.sta.delete.Delete.query")
    @mock.patch("stapy.cli.cli.cprompt")
    def test_delete_request(self, mocked_prompt, mocked_del_q, mocked_del_e):
        ids = ["1", "4", "5"]
        mocked_prompt.side_effect = ["DELETE", "IDs", "Datastream", " ".join(ids), False]
        CLI()
        params, kparams = mocked_del_e.call_args
        self.assertEqual(params[0], Entity.Datastream)
        self.assertEqual(params[1], ids)

        path = "Datastreams(15)/Observations"
        mocked_prompt.side_effect = ["DELETE", "Path", path, False]
        CLI()
        params, kparams = mocked_del_q.call_args
        self.assertEqual(params[0], path)

    @mock.patch("stapy.cli.cli.cprompt")
    def test_get_request(self, mocked_prompt):
        mocked_prompt.side_effect = ["GET", False]
        with self.assertRaises(Exception):
            CLI()

    def test_cap_first(self):
        self.assertEqual(cap_first("test"), "Test")
        self.assertEqual(cap_first("Test"), "Test")
        self.assertEqual(cap_first(0), "")

    @mock.patch("PyInquirer.prompt")
    def test_cprompt(self, mocked_prompt):
        mocked_prompt.side_effect = {}
        with self.assertRaises(SystemExit):
            cprompt("", True)


if __name__ == '__main__':
    unittest.main()
