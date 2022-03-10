import unittest
import logging

from stapy.sta.request import Request

logging.disable(logging.CRITICAL)

class TestSTAMethods(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_list(self):
        # self.assertEqual(len(Request), len(Request.list()))
        self.assertIn(Request.POST.value, Request.list())


if __name__ == "__main__":
    unittest.main()
