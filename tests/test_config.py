import unittest
import os

from stapy.common.config import config, Config, set_api_url

class TestConfigMethods(unittest.TestCase):

    filename = "test.ini"
    config = None

    def setUp(self):
        os.mknod(self.filename)
        self.config = Config(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_read(self):
        name = "xyz.ini"
        config = Config(name)

    def test_save(self):
        config.save()

    def test_set(self):
        self.config.set(test="testing")
        self.config.set(var={"test": "test"})

    def test_get(self):
        self.config.set(test="testing")
        self.config.set(var={"test": "test"})
        self.assertEqual(self.config.get("test"), "testing")
        self.assertEqual(self.config.get("var"), str({"test": "test"}))
        self.assertEqual(self.config.get("xyz"), "")

    def test_set_api_url(self):
        before = config.get("API_URL")
        set_api_url(10)
        after = config.get("API_URL")
        self.assertEqual(before, after)
        set_api_url("localhost:8080/FROST-Server/v1.1")
        first = config.get("API_URL")
        set_api_url("localhost:8080/FROST-Server/v1.1/")
        second = config.get("API_URL")
        self.assertEqual(first, second)


if __name__ == '__main__':
    unittest.main()
