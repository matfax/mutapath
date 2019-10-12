import unittest

from mutapath import MutaPath


class TestMutaPath(unittest.TestCase):
    def _gen_start_path(self):
        self.test_base = MutaPath.getcwd().joinpath("mutapath_test")
        self.test_base.mkdir()
        new_file = self.test_base.joinpath("test.file")
        new_file.touch()
        return new_file

    def _clean(self):
        self.test_base.rmtree_p()

    def test_suffix(self):
        try:
            test_file = self._gen_start_path()
            expected = ".file"
            actual = test_file.suffix
            self.assertEqual(expected, actual)
        finally:
            self._clean()

    def test_set_suffix(self):
        try:
            test_file = self._gen_start_path()
            expected = ".txt"
            test_file.suffix = expected
            actual = test_file.suffix
            self.assertEqual(expected, actual)
        finally:
            self._clean()

    def test_name(self):
        try:
            test_file = self._gen_start_path()
            expected = "test.file"
            actual = test_file.name
            self.assertEqual(expected, actual)
        finally:
            self._clean()

    def test_set_name(self):
        try:
            test_file = self._gen_start_path()
            expected = "new.txt"
            test_file.name = expected
            actual = test_file.name
            self.assertEqual(expected, actual)
        finally:
            self._clean()

    def test_base(self):
        try:
            test_file = self._gen_start_path()
            expected = self.test_base
            actual = test_file.base
            self.assertEqual(expected, actual)
        finally:
            self._clean()

    def test_rename(self):
        try:
            test_file = self._gen_start_path()
            expected = test_file.with_name("new.txt")
            test_file.rename(expected)
            actual = test_file
            self.assertEqual(expected, actual)
        finally:
            self._clean()

    def test_renames(self):
        try:
            test_file = self._gen_start_path()
            expected = test_file.parent.joinpath("other/new")
            test_file.renames(expected)
            actual = test_file
            self.assertEqual(expected, actual)
        finally:
            self._clean()

    def test_copy(self):
        try:
            test_file = self._gen_start_path()
            expected = test_file.with_name("new.txt")
            test_file.copy(expected)
            actual = test_file
            self.assertEqual(expected, actual)
        finally:
            self._clean()

    def test_copy2(self):
        try:
            test_file = self._gen_start_path()
            expected = test_file.parent.joinpath("other/new")
            expected.parent.mkdir()
            test_file.copy2(expected)
            actual = test_file
            self.assertEqual(expected, actual)
        finally:
            self._clean()

    def test_copyfile(self):
        try:
            test_file = self._gen_start_path()
            expected = test_file.parent.joinpath("new.file")
            test_file.copyfile(expected)
            actual = test_file
            self.assertEqual(expected, actual)
        finally:
            self._clean()

    def test_copytree(self):
        try:
            test_file = self._gen_start_path()
            from_here = self.test_base.joinpath("from/here")
            from_here.makedirs()
            test_file.copy(from_here)
            expected = self.test_base.joinpath("to")
            from_here.copytree(expected)
            self.assertEqual(expected, from_here)
        finally:
            self._clean()

    def test_move(self):
        try:
            test_file = self._gen_start_path()
            from_here = self.test_base.joinpath("from/here")
            from_here.makedirs()
            test_file.copy(from_here)
            expected = self.test_base.joinpath("to")
            from_here.move(expected)
            self.assertEqual(expected, from_here)
        finally:
            self._clean()

    def test_merge_tree(self):
        try:
            test_file = self._gen_start_path()
            from_here = self.test_base.joinpath("from/here")
            from_here.makedirs()
            test_file.copy(from_here)
            expected = self.test_base.joinpath("to")
            from_here.merge_tree(expected)
            self.assertEqual(expected, from_here)
        finally:
            self._clean()
