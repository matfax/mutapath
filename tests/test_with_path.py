import unittest

from mutapath import Path
from mutapath.exceptions import PathException


class TestWithPath(unittest.TestCase):
    def _gen_start_path(self):
        self.test_base = Path.getcwd() / "mutapath_with_test"
        self.test_base.rmtree_p()
        self.test_base.mkdir()
        new_file = self.test_base / "test.file"
        new_file.touch()
        return new_file

    def _clean(self):
        self.test_base.rmtree_p()

    def test_mutate(self):
        try:
            test_file = self._gen_start_path()
            expected = test_file.with_name("new.txt")
            with test_file.mutate() as mut:
                mut.stem = "new"
                mut.suffix = ".txt"
            actual = test_file
            self.assertEqual(expected, actual)
        finally:
            self._clean()

    def test_renaming(self):
        try:
            test_file = self._gen_start_path()
            expected = test_file.with_name("new.txt")
            with test_file.renaming() as mut:
                mut.stem = "new"
                mut.suffix = ".txt"
            actual = test_file
            self.assertEqual(expected, actual)
            self.assertTrue(actual.exists(), "File has to exist")
        finally:
            self._clean()

    def test_rename_in_mutate(self):
        try:
            test_file = self._gen_start_path()
            expected = test_file.with_name("new.txt")
            with test_file.mutate() as mut:
                mut.rename(expected)
            actual = test_file
            self.assertEqual(expected, actual)
            self.assertTrue(actual.exists(), "File has to exist")
        finally:
            self._clean()

    def test_rename_fail(self):
        try:
            test_file = self._gen_start_path()
            wrong = test_file.with_name("new.txt")
            expected = test_file.normpath()
            test_file.copy(wrong)
            with self.assertRaises(PathException):
                with test_file.renaming() as mut:
                    mut.name = wrong.name
            actual = test_file
            self.assertEqual(expected, actual)
            self.assertTrue(actual.exists(), "File has to exist")
        finally:
            self._clean()

    def test_copying(self):
        try:
            test_file = self._gen_start_path()
            expected = test_file.with_name("new.txt")
            with test_file.copying() as mut:
                mut.stem = "new"
                mut.suffix = ".txt"
            actual = test_file
            self.assertEqual(expected, actual)
            self.assertEqual(test_file.text(), actual.text())
            self.assertTrue(actual.exists(), "File has to exist")
        finally:
            self._clean()

    def test_move(self):
        try:
            test_file = self._gen_start_path()
            from_here = self.test_base / "from/here"
            from_here.makedirs()
            test_file.copy(from_here)
            expected = self.test_base / "to"
            with from_here.moving() as mut:
                mut.joinpath(self.test_base, "to")
            self.assertEqual(expected, from_here)
            self.assertTrue(from_here.exists(), "File has to exist")
        finally:
            self._clean()
