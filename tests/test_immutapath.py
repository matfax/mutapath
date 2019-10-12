import os
import unittest

from mutapath import Path


class TestPath(unittest.TestCase):
    def test_with_name_posix(self):
        expected = Path("/A/B/other")
        actual = Path("/A/B/test1.txt").with_name("other")
        self.assertEqual(expected.normpath(), actual.normpath())

    def test_with_name_win(self):
        if os.name == 'nt':
            expected = Path("C:/B/other")
            actual = Path("C:/B/test1.txt").with_name("other")
            self.assertEqual(expected.abspath(), actual.abspath())

    def test_with_base_posix(self):
        expected = Path("/home/joe/folder/sub")
        actual = Path("/home/doe/folder/sub").with_base("/home/joe")
        self.assertEqual(expected.normpath(), actual.normpath())

    def test_with_base_length_posix(self):
        expected = Path("/home/joe/doe/folder/sub")
        actual = Path("/home/doe/folder/sub").with_base("/home/joe", 1)
        self.assertEqual(expected.normpath(), actual.normpath())

    def test_with_base_win(self):
        if os.name == 'nt':
            expected = Path("C:/Users/joe/folder/sub")
            actual = Path("C:/Users/doe/folder/sub").with_base("C:/Users/joe")
            self.assertEqual(expected.normpath(), actual.normpath())

    def test_with_base_length_win(self):
        if os.name == 'nt':
            expected = Path("C:/Users/joe/doe/folder/sub").abspath()
            actual = Path("C:/Users/doe/folder/sub").abspath().with_base("C:/Users/joe", 1)
            self.assertEqual(expected.normpath(), actual.normpath())
