import time
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

    def test_wrapped_iterable(self):
        try:
            test_file = self._gen_start_path()
            expected = [test_file]
            actual = self.test_base.listdir()
            self.assertEqual(expected, actual)
            self.assertIsInstance(actual[0], Path)
        finally:
            self._clean()

    def test_wrapped_generator(self):
        try:
            test_file = self._gen_start_path()
            expected = [test_file]
            actual = list(self.test_base.walk())
            self.assertEqual(expected, actual)
            self.assertIsInstance(actual[0], Path)
        finally:
            self._clean()

    def test_open(self):
        try:
            test_file = self._gen_start_path()
            expected = "test"
            with test_file.open("w") as w:
                w.write(expected)
            actual = test_file.text()
            self.assertEqual(expected, actual)
            self.assertIsInstance(test_file, Path)
        finally:
            self._clean()

    def test_size(self):
        try:
            test_file = self._gen_start_path()
            expected = 0
            actual = test_file.size
            self.assertEqual(expected, actual)
            self.assertIsInstance(test_file, Path)
        finally:
            self._clean()

    def test_mtime(self):
        try:
            test_file = self._gen_start_path()
            actual = test_file.mtime
            time.sleep(0.1)
            other = test_file.with_name("other.txt").touch()
            later = other.mtime
            self.assertGreater(later, actual)
            test_file.copystat(other)
            later = other.mtime
            self.assertEqual(later, actual)
        finally:
            self._clean()

    def test_ctime(self):
        try:
            test_file = self._gen_start_path()
            actual = test_file.ctime
            time.sleep(0.1)
            other = test_file.with_name("other.txt").touch()
            later = other.ctime
            self.assertGreater(later, actual)
        finally:
            self._clean()

    def test_atime(self):
        try:
            test_file = self._gen_start_path()
            actual = test_file.atime
            other = test_file.copy2(test_file.with_name("other.txt"))
            later = other.atime
            self.assertEqual(later, actual)
        finally:
            self._clean()

    def test_mutate(self):
        try:
            test_file = self._gen_start_path()
            expected = test_file.with_name("new.txt")
            with test_file.mutate() as mut:
                mut.stem = "new"
                mut.suffix = ".txt"
            actual = test_file
            self.assertEqual(expected, actual)
            self.assertIsInstance(actual, Path)
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
            self.assertIsInstance(actual, Path)
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
            self.assertIsInstance(actual, Path)
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
            self.assertIsInstance(actual, Path)
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
            self.assertIsInstance(actual, Path)
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
            self.assertIsInstance(from_here, Path)
            self.assertTrue(from_here.exists(), "File has to exist")
        finally:
            self._clean()
