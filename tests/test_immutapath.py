import os
import pathlib
import unittest

import path

from mutapath import Path, MutaPath


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

    def test_with_base_fail(self):
        def too_long():
            Path("/A/B/other.txt").with_base("/A/B/C")

        self.assertRaises(ValueError, too_long)

    def test_with_stem(self):
        expected = Path("/A/B/other.txt")
        actual = Path("/A/B/test1.txt").with_stem("other")
        self.assertEqual(expected.normpath(), actual.normpath())

    def test_with_parent(self):
        other = Path("/A/D/other.txt")
        expected = Path("D/other.txt")
        actual = Path("/A/B/other.txt").with_parent(other.dirname.name)
        self.assertEqual(expected.normpath(), actual.normpath())

    def test_static_joinpath(self):
        expected = Path("/A/B/C/D/other.txt")
        actual = Path.joinpath("/A/B", "C/", Path("D"), MutaPath("other.txt"))
        self.assertEqual(expected.normpath(), actual.normpath())

    def test_joinpath(self):
        expected = Path("/A/B/C/D/other.txt")
        actual = Path("/A/B").joinpath("C", Path("D"), MutaPath("other.txt"))
        self.assertEqual(expected.normpath(), actual.normpath())

    def test_pathlib_path(self):
        expected = Path("/A/B/other.txt")
        actual = Path(pathlib.Path("/A/B")).joinpath(pathlib.PurePosixPath("other.txt"))
        self.assertEqual(expected.normpath(), actual.normpath())

    def test_block_setter(self):
        some = Path("/A/B/other.txt")

        def set_name():
            some.name = "try"

        self.assertRaises(AttributeError, set_name)

    def test_eq(self):
        some = Path("/A/B/other.txt")
        other = path.Path("/A/B/other.txt")
        third = pathlib.Path("/A/B/other.txt")
        self.assertEqual(some, other)
        self.assertEqual(some, third)

    def test_add(self):
        expected = Path("/A/B/other.txt")
        actual = Path("/A/") + "/B/" + "/other.txt"
        self.assertEqual(expected, actual)

    def test_radd(self):
        expected = Path("/A/B/other.txt")
        actual = "/A/" + Path("/B/") + "/other.txt"
        self.assertEqual(expected, actual)

    def test_div(self):
        expected = Path("/A/B/other.txt")
        actual = Path("/A/") / "B/other.txt"
        self.assertEqual(expected, actual)

    def test_rdiv(self):
        expected = Path("/A/B/other.txt")
        actual = "/A/" / Path("B") / "other.txt"
        self.assertEqual(expected, actual)

    def test_capsulation(self):
        excpected = Path("/A/B")
        actual = Path(Path(excpected))
        self.assertEqual(excpected, actual)

    def test_repr(self):
        excpected = Path("/A/B")
        self.assertTrue(repr(excpected).startswith("Path"))
