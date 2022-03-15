import os
import logging
import requests
import unittest

from stapy.common.config import config, Config, set_log_level, set_sta_url, set_credentials

logging.disable(logging.CRITICAL)

class TestConfigMethods(unittest.TestCase):

    filename = "test.ini"
    config = None
    url = None

    @classmethod
    def setUpClass(cls):
        cls.url = config.load_sta_url()

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
        self.assertEqual(self.config.get("xyz"), None)

    def test_log_lvl(self):
        config.remove("LOG_LVL")
        self.assertEqual(config.load_log_lvl(), 30)
        set_log_level("INFO")
        self.assertEqual(config.load_log_lvl(), 30)
        set_log_level(20)
        self.assertEqual(config.load_log_lvl(), 20)

    def test_set_sta_url(self):
        before = config.load_sta_url()
        set_sta_url(10)
        after = config.load_sta_url()
        self.assertEqual(before, after)
        set_sta_url("localhost:8080/FROST-Server/v1.1")
        first = config.load_sta_url()
        set_sta_url("localhost:8080/FROST-Server/v1.1/")
        second = config.load_sta_url()
        self.assertEqual(first, second)

    def test_credentials(self):
        config.remove("STA_USR")
        config.remove("STA_PWD")
        self.assertEqual(config.load_authentication(), None)
        usr = "username"
        pwd = "password"
        set_credentials(usr, pwd)
        self.assertEqual(config.load_authentication(), requests.auth.HTTPBasicAuth(usr, pwd))


if __name__ == "__main__":
    unittest.main()
