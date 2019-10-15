import unittest

from mutapath import MutaPath, Path


class TestMutaPath(unittest.TestCase):
    def _gen_start_path(self):
        self.test_base = Path.getcwd() / "mutapath_test"
        self.test_base.mkdir()
        new_file = self.test_base / "test.file"
        new_file.touch()
        return MutaPath(new_file)

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

    def test_set_base(self):
        expected = Path("/A/D/other.txt")
        actual = MutaPath("/A/B/other.txt")
        actual.base = "/A/D"
        self.assertEqual(expected, actual)

    def test_set_stem(self):
        expected = Path("/A/B/other2.txt")
        actual = MutaPath("/A/B/other.txt")
        actual.stem += "2"
        self.assertEqual(expected, actual)

    def test_set_parent(self):
        expected = Path("/A/B/C/other.txt")
        actual = MutaPath("/A/other.txt")
        actual.parent /= "B/C"
        self.assertEqual(expected, actual)

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
            expected = test_file.parent / "other/new"
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
            expected = test_file.parent / "other/new"
            expected.parent.mkdir()
            test_file.copy2(expected)
            actual = test_file
            self.assertEqual(expected, actual)
        finally:
            self._clean()

    def test_copyfile(self):
        try:
            test_file = self._gen_start_path()
            expected = test_file.parent / "new.file"
            test_file.copyfile(expected)
            actual = test_file
            self.assertEqual(expected, actual)
        finally:
            self._clean()

    def test_copytree(self):
        try:
            test_file = self._gen_start_path()
            from_here = ~ (self.test_base / "from/here")
            from_here.makedirs()
            test_file.copy(from_here)
            expected = self.test_base / "to"
            from_here.copytree(expected)
            self.assertEqual(expected, from_here)
        finally:
            self._clean()

    def test_move(self):
        try:
            test_file = self._gen_start_path()
            from_here = ~ (self.test_base / "from/here")
            from_here.makedirs()
            test_file.copy(from_here)
            expected = self.test_base / "to"
            from_here.move(expected)
            self.assertEqual(expected, from_here)
        finally:
            self._clean()

    def test_merge_tree(self):
        try:
            test_file = self._gen_start_path()
            from_here = ~ (self.test_base / "from/here")
            from_here.makedirs()
            test_file.copy(from_here)
            expected = self.test_base / "to"
            from_here.merge_tree(expected)
            self.assertEqual(expected, from_here)
        finally:
            self._clean()

    def test_static_joinpath(self):
        expected = MutaPath("/A/B/C/D/other.txt")
        actual = MutaPath.joinpath("/A/B", "C/", MutaPath("D"), Path("other.txt"))
        self.assertEqual(expected.normpath(), actual.normpath())

    def test_joinpath(self):
        expected = MutaPath("/A/B/C/D/other.txt")
        actual = MutaPath("/A/B").joinpath("C", MutaPath("D"), Path("other.txt"))
        self.assertEqual(expected.normpath(), actual.normpath())

    def test_capsulation(self):
        expected = MutaPath("/A/B")
        actual = MutaPath(MutaPath(expected))
        self.assertEqual(expected, actual)

    def test_repr(self):
        excpected = MutaPath("/A/B")
        self.assertTrue(repr(excpected).startswith("Path"))

    def test_hash(self):
        expected = hash(Path("/A/B"))
        actual = hash(MutaPath("/A/B/"))
        self.assertEqual(expected, actual)
