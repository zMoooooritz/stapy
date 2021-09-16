import unittest

from stapy.common.log import Log, custom_logger

class TestLogMethods(unittest.TestCase):

    def test_from_string(self):
        self.assertEquals(Log.ERROR, Log.from_string("ERROR"))
        self.assertEquals(Log.NOTSET, Log.from_string("XYZ"))

    def test_custom_logger(self):
        custom_logger('root', Log.INFO.value)
        with self.assertRaises(Exception):
            custom_logger('root', Log.INFO)
        with self.assertRaises(Exception):
            custom_logger('root')


if __name__ == '__main__':
    unittest.main()
