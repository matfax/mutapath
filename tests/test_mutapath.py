from mutapath import MutaPath, Path
from tests.helper import PathTest, file_test

file_test_no_asserts = file_test(equal=False, instance=False, exists=False, posix_test=False, string_test=False)


class TestMutaPath(PathTest):
    def __init__(self, *args):
        self.test_path = "mutapath_test"
        super().__init__(*args)

    def _gen_start_path(self, posix: bool = False, use_string: bool = False):
        return MutaPath(super(TestMutaPath, self)._gen_start_path(posix), posix=posix, string_repr=use_string)

    @file_test_no_asserts
    def test_suffix(self, test_file: Path):
        expected = ".file"
        actual = test_file.suffix
        self.assertEqual(expected, actual)

    @file_test_no_asserts
    def test_set_suffix(self, test_file: Path):
        expected = ".txt"
        test_file.suffix = expected
        actual = test_file.suffix
        self.assertEqual(expected, actual)

    @file_test_no_asserts
    def test_name(self, test_file: Path):
        expected = "test.file"
        actual = test_file.name
        self.assertEqual(expected, actual)
        self.assertIsInstance(actual, Path)

    @file_test_no_asserts
    def test_set_name(self, test_file: Path):
        expected = "new.txt"
        test_file.name = expected
        actual = test_file.name
        self.assertEqual(expected, actual)
        self.assertIsInstance(test_file, MutaPath)

    @file_test_no_asserts
    def test_base(self, test_file: Path):
        expected = self.test_base
        actual = test_file.base
        self.assertEqual(expected, actual)
        self.assertIsInstance(actual, Path)

    def test_set_base(self):
        expected = Path("/A/D/other.txt")
        actual = MutaPath("/A/B/other.txt")
        actual.base = "/A/D"
        self.assertEqual(expected, actual)
        self.assertIsInstance(actual, MutaPath)

    def test_set_stem(self):
        expected = Path("/A/B/other2.txt")
        actual = MutaPath("/A/B/other.txt")
        actual.stem += "2"
        self.assertEqual(expected, actual)
        self.assertIsInstance(actual, MutaPath)

    def test_set_parent(self):
        expected = Path("/A/B/C/other.txt")
        actual = MutaPath("/A/other.txt")
        actual.parent /= "B/C"
        self.assertEqual(expected, actual)
        self.assertIsInstance(actual, MutaPath)

    def test_set_posix_enabled(self):
        expected = Path("/A/B/C/other.txt", posix=True)
        actual = MutaPath("/A/B/C/other.txt")
        actual.posix_enabled = True
        self.assertEqual(expected, actual)
        self.assertIsInstance(actual, MutaPath)

    @file_test()
    def test_rename(self, test_file: Path):
        expected = test_file.with_name("new.txt")
        test_file.rename(expected)
        self.assertIsInstance(test_file, MutaPath)
        return expected

    @file_test()
    def test_renames(self, test_file: Path):
        expected = test_file.parent / "other/new"
        test_file.renames(expected)
        self.assertIsInstance(test_file, MutaPath)
        return expected

    @file_test()
    def test_copy(self, test_file: Path):
        expected = test_file.with_name("new.txt")
        test_file.copy(expected)
        self.assertIsInstance(test_file, MutaPath)
        return expected

    @file_test()
    def test_copy2(self, test_file: Path):
        expected = test_file.parent / "other/new"
        expected.parent.mkdir()
        test_file.copy2(expected)
        self.assertIsInstance(test_file, MutaPath)
        return expected

    @file_test()
    def test_copyfile(self, test_file: Path):
        expected = test_file.parent / "new.file"
        test_file.copyfile(expected)
        self.assertIsInstance(test_file, MutaPath)
        return expected

    @file_test(equal=False)
    def test_copytree(self, test_file: Path):
        from_here = ~ (self.test_base / "from/here")
        from_here.makedirs()
        test_file.copy(from_here)
        expected = self.test_base / "to"
        from_here.copytree(expected)
        self.assertEqual(expected, from_here)
        self.assertIsInstance(from_here, MutaPath)

    @file_test(equal=False, exists=False)
    def test_move(self, test_file: Path):
        from_here = self.test_base / "from/here"
        current = ~ from_here
        current.makedirs()
        test_file.copy(current)
        expected = self.test_base / "to"
        current.move(expected)
        self.assertEqual(expected, current)
        self.assertIsInstance(current, MutaPath)
        self.assertTrue(not from_here.exists(), "The moved file still exists in the source folder.")
        target_not_empty = len(current.files("test.file*")) > 0
        self.assertTrue(target_not_empty, "The target file does not exist.")

    @file_test(equal=False)
    def test_merge_tree(self, test_file: Path):
        from_here = ~ (self.test_base / "from/here")
        from_here.makedirs()
        test_file.copy(from_here)
        expected = self.test_base / "to"
        from_here.merge_tree(expected)
        self.assertEqual(expected, from_here)
        self.assertIsInstance(from_here, MutaPath)

    def test_static_joinpath(self):
        expected = MutaPath("/A/B/C/D/other.txt")
        actual = MutaPath.joinpath("/A/B", "C/", MutaPath("D"), Path("other.txt"))
        self.assertEqual(expected.normpath(), actual.normpath())
        self.assertIsInstance(actual, MutaPath)

    def test_joinpath(self):
        expected = MutaPath("/A/B/C/D/other.txt")
        actual = MutaPath("/A/B").joinpath("C", MutaPath("D"), Path("other.txt"))
        self.assertEqual(expected.normpath(), actual.normpath())
        self.assertIsInstance(actual, MutaPath)

    def test_capsulation(self):
        expected = MutaPath("/A/B")
        actual = MutaPath(MutaPath(expected))
        self.assertEqual(expected, actual)

    def test_repr(self):
        expected = "Path('/A/B')"
        actual = MutaPath("/A/B", posix=True)
        self.assertEqual(expected, repr(actual))

    def test_hash(self):
        expected = hash(Path("/A/B"))
        actual = hash(MutaPath("/A/B/"))
        self.assertEqual(expected, actual)
