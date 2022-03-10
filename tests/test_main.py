import unittest
import logging
from unittest import mock

from stapy.common.log import Log
from stapy.cli.main import main

logging.disable(logging.CRITICAL)

class TestMain(unittest.TestCase):

    @mock.patch("stapy.cli.parser.Parser.parse_args")
    @mock.patch("stapy.cli.parser.Parser.get_log_level")
    @mock.patch("stapy.cli.parser.Parser.__init__")
    def test(self, mocked_init, mocked_log, mocked_args):
        mocked_init.return_value = None
        mocked_log.return_value = Log.WARNING.value
        main()


if __name__ == "__main__":
    unittest.main()
