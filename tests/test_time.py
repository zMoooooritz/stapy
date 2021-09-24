import unittest

from stapy.sta.time import Time

class TestTimeMethods(unittest.TestCase):

    def setUp(self):
        self.str1 = "22:22:22 01.01.2020" 
        self.str2 = "01.01.2010 22:22:22" 

    def test_time(self):
        with self.assertRaises(Exception):
            Time(123)
        self.assertEqual(str(Time(self.str1)), "2020-01-01T22:22:22")
        self.assertEqual(str(Time(self.str1 + "-" + self.str2)), "2010-01-01T22:22:22-2020-01-01T22:22:22")
        self.assertEqual(str(Time(self.str1 + "-" + self.str2)), str(Time(self.str2 + "-" + self.str1)))
        self.assertEqual(str(Time("-" + self.str1)), "2020-01-01T22:22:22")
        self.assertEqual(str(Time(self.str1 + "-" + self.str1)), "2020-01-01T22:22:22")


if __name__ == '__main__':
    unittest.main()
