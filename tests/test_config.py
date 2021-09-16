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
        os.remove(self.filename)

    def test_save(self):
        config.save()

    def test_set(self):
        config.set(test="testing")
        config.set(var={"test": "test"})

    def test_get(self):
        self.config.set(test="testing")
        self.config.set(var={"test": "test"})
        self.assertEqual(self.config.get("test"), "testing")
        self.assertEqual(self.config.get("var"), str({"test": "test"}))

    def test_set_api_url(self):
        set_api_url("localhost:8080/FROST-Server/v1.1")
        first = config.get("API_URL")
        set_api_url("localhost:8080/FROST-Server/v1.1/")
        second = config.get("API_URL")
        self.assertEqual(first, second)


if __name__ == '__main__':
    unittest.main()
