import unittest

from stapy.sta.time import Time

class TestTimeMethods(unittest.TestCase):

    def setUp(self):
        self.str1 = "2020-03-31 12:34:56"
        self.str2 = "12:34:56 2020-12-24"

    def test_time(self):
        with self.assertRaises(Exception):
            Time(123)
        self.assertEqual(str(Time(self.str1)), "2020-03-31T12:34:56")
        self.assertEqual(str(Time(self.str1 + "/" + self.str2)), "2020-03-31T12:34:56/2020-12-24T12:34:56")
        self.assertEqual(str(Time(self.str1 + "/" + self.str2)), str(Time(self.str2 + "/" + self.str1)))
        self.assertEqual(str(Time("/" + self.str1)), "2020-03-31T12:34:56")
        self.assertEqual(str(Time(self.str1 + "/" + self.str1)), "2020-03-31T12:34:56")
        self.assertEqual(str(Time("31.03.2020 12:34:56")), "2020-03-31T12:34:56")


if __name__ == "__main__":
    unittest.main()
