import os
import logging
import unittest

from stapy.common.config import config, Config, set_sta_url

logging.disable(logging.CRITICAL)

class TestConfigMethods(unittest.TestCase):

    filename = "test.ini"
    config = None
    url = None

    @classmethod
    def setUpClass(cls):
        cls.url = config.get("sta_url")

    def setUp(self):
        os.mknod(self.filename)
        self.config = Config(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    @classmethod
    def tearDownClass(cls):
        config.set(sta_url=cls.url)

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

    def test_set_sta_url(self):
        before = config.get("STA_URL")
        set_sta_url(10)
        after = config.get("STA_URL")
        self.assertEqual(before, after)
        set_sta_url("localhost:8080/FROST-Server/v1.1")
        first = config.get("STA_URL")
        set_sta_url("localhost:8080/FROST-Server/v1.1/")
        second = config.get("STA_URL")
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
