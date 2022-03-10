import unittest
import logging

from stapy.common.log import Log, create_logger

logging.disable(logging.CRITICAL)

class TestLogMethods(unittest.TestCase):

    def test_from_string(self):
        self.assertEqual(Log.ERROR, Log.from_string("ERROR"))
        self.assertEqual(Log.NOTSET, Log.from_string("XYZ"))

    def test_custom_logger(self):
        create_logger(Log.INFO.value)

if __name__ == "__main__":
    unittest.main()
