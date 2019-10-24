import os
import pathlib

import path

from mutapath import Path, MutaPath, PathDefaults
from tests.helper import PathTest


class TestPath(PathTest):
    def test_with_name_posix(self):
        expected = Path("/A/B/other")
        actual = Path("/A/B/test1.txt").with_name("other")
        self.assertEqual(expected, actual)
        self.typed_instance_test(actual)

    def test_with_name_win(self):
        if os.name == 'nt':
            expected = Path("C:/B/other")
            actual = Path("C:/B/test1.txt").with_name("other")
            self.assertEqual(expected, actual)
            self.typed_instance_test(actual)

    def test_with_base_posix(self):
        expected = Path("/home/joe/folder/sub")
        actual = Path("/home/doe/folder/sub").with_base("/home/joe")
        self.assertEqual(expected, actual)
        self.typed_instance_test(actual)

    def test_with_base_length_posix(self):
        expected = Path("/home/joe/doe/folder/sub")
        actual = Path("/home/doe/folder/sub").with_base("/home/joe", 1)
        self.assertEqual(expected, actual)
        self.typed_instance_test(actual)

    def test_with_base_win(self):
        if os.name == 'nt':
            expected = Path("C:/Users/joe/folder/sub")
            actual = Path("C:/Users/doe/folder/sub").with_base("C:/Users/joe")
            self.assertEqual(expected, actual)
            self.typed_instance_test(actual)

    def test_with_base_length_win(self):
        if os.name == 'nt':
            expected = Path("C:/Users/joe/doe/folder/sub").abspath()
            actual = Path("C:/Users/doe/folder/sub").abspath().with_base("C:/Users/joe", 1)
            self.assertEqual(expected, actual)
            self.typed_instance_test(actual)

    def test_with_base_fail(self):
        with self.assertRaises(ValueError):
            Path("/A/B/other.txt").with_base("/A/B/C")

    def test_with_stem(self):
        expected = Path("/A/B/other.txt")
        actual = Path("/A/B/test1.txt").with_stem("other")
        self.assertEqual(expected, actual)
        self.typed_instance_test(actual)

    def test_with_parent(self):
        other = Path("/A/D/other.txt")
        expected = Path("D/other.txt")
        actual = Path("/A/B/other.txt").with_parent(other.dirname.name)
        self.assertEqual(expected, actual)
        self.typed_instance_test(actual)

    @staticmethod
    def _string_repr_enabled(path: Path):
        return path.string_repr_enabled

    def test_with_string_repr_enabled(self):
        self.arg_with_matrix(Path.with_string_repr_enabled, self._string_repr_enabled, string_repr=False)
        self.arg_with_matrix(Path.with_string_repr_enabled, self._string_repr_enabled, string_repr=False, posix=False)
        self.arg_with_matrix(Path.with_string_repr_enabled, self._string_repr_enabled, string_repr=False, posix=True)

    def test_defaults_with_string_repr(self):
        getter = lambda p: p.string_repr_enabled
        PathDefaults().string_repr = True
        self.arg_with_matrix(Path.with_string_repr_enabled, getter, string_repr=True)
        self.arg_with_matrix(Path.with_string_repr_enabled, getter, string_repr=True, posix=False)
        self.arg_with_matrix(Path.with_string_repr_enabled, getter, string_repr=True, posix=True)
        PathDefaults().reset()

    def test_with_posix_enabled(self):
        getter = lambda p: p.posix_enabled
        self.arg_with_matrix(Path.with_poxis_enabled, getter, posix=False)
        self.arg_with_matrix(Path.with_poxis_enabled, getter, posix=False, string_repr=False)
        self.arg_with_matrix(Path.with_poxis_enabled, getter, posix=False, string_repr=True)

    def test_defaults_with_posix(self):
        getter = lambda p: p.posix_enabled
        PathDefaults().posix = True
        self.arg_with_matrix(Path.with_poxis_enabled, getter, posix=True)
        self.arg_with_matrix(Path.with_poxis_enabled, getter, posix=True, string_repr=False)
        self.arg_with_matrix(Path.with_poxis_enabled, getter, posix=True, string_repr=True)
        PathDefaults().reset()

    def test_static_joinpath(self):
        expected = Path("/A/B/C/D/other.txt")
        actual = Path.joinpath("/A/B", "C/", Path("D"), MutaPath("other.txt"))
        self.assertEqual(expected, actual)
        self.typed_instance_test(actual)

    def test_joinpath(self):
        expected = Path("/A/B/C/D/other.txt")
        actual = Path("/A/B").joinpath("C", Path("D"), MutaPath("other.txt"))
        self.assertEqual(expected, actual)
        self.typed_instance_test(actual)

    def test_clone(self):
        expected = Path("/A/B/C/D/other.txt", posix=True)
        actual = Path("/A/B/other.txt", posix=True).clone("/A/B/C/D/other.txt")
        self.assertEqual(expected, actual)
        self.typed_instance_test(actual)

    def test_pathlib_path(self):
        expected = Path("/A/B/other.txt")
        actual = Path(pathlib.Path("/A/B")).joinpath(pathlib.PurePosixPath("other.txt"))
        self.assertEqual(expected, actual)
        self.typed_instance_test(actual)

    def test_block_setter(self):
        some = Path("/A/B/other.txt")
        with self.assertRaises(AttributeError):
            some.name = "try"

    def test_not_eq(self):
        some = Path("/A/B/other.txt")
        self.assertNotEqual(some, 42)

    def test_eq(self):
        def posix_path(contain):
            return Path(contain, posix=True)

        constructors = [posix_path, Path, MutaPath]
        comparable_constructors = constructors + [path.Path, pathlib.Path, str]
        containers = ["/A/B/other.txt"]
        if os.name == 'nt':
            containers += ["/A\\B/other.txt", "\\A\\B\\other.txt"]

        paths = list()
        comparables = list()

        for cont in containers:
            for const in constructors:
                paths.append((const, const(cont)))
                for nested in constructors:
                    paths.append((f"Path(({const}, posix)", nested(const(cont))))
            for comp in comparable_constructors:
                comparables.append((comp, comp(cont)))

        for l_const, l in paths:
            for r_const, r in comparables:
                self.assertEqual(l, r, f"{l_const} is not equalling comparable {r_const}")

    def test_add(self):
        expected = "/A/B/other.txt"
        actual = Path("/A/", posix=True) + "/B/" + "/other.txt"
        self.assertEqual(expected, actual)
        self.assertIsInstance(actual, str)

    def test_radd(self):
        expected = "/A/B/other.txt"
        actual = "/A/" + Path("/B/other.txt", posix=True)
        self.assertEqual(expected, actual)
        self.assertIsInstance(actual, str)

    def test_div(self):
        expected = Path("/A/B/other.txt")
        actual = Path("/A/") / "B/other.txt"
        self.assertEqual(expected, actual)
        self.typed_instance_test(actual)

    def test_rdiv(self):
        expected = Path("/A/B/other.txt")
        actual = "/A/" / Path("B") / "other.txt"
        self.assertEqual(expected, actual)
        self.typed_instance_test(actual)

    def test_capsulation(self):
        excpected = Path("/A/B")
        actual = Path(Path(excpected))
        self.assertEqual(excpected, actual)
        self.typed_instance_test(actual)

    def test_repr(self):
        expected = "Path('/A/B')"
        actual = Path("\\A\\B", posix=True)
        self.assertEqual(repr(actual), expected)

    def test_string_repr(self):
        expected = "/A/B"
        actual = Path("\\A\\B", posix=True, string_repr=True)
        self.assertEqual(repr(actual), expected)

    def test_str(self):
        expected = "/A/B"
        actual = Path("\\A\\B", posix=True)
        self.assertEqual(str(actual), expected)

    def test_parents(self):
        excpected = [Path("/A/B/C"), Path("/A/B"), Path("/A"), Path("/")]
        actual = list(Path("/A/B/C/D").parents)
        self.assertEqual(excpected, actual)
        self.typed_instance_test(actual[0])

    def test_anchor(self):
        if os.name == 'nt':
            excpected = "C:\\"
            actual = Path("C:/A/B/C").anchor
        else:
            excpected = "/"
            actual = Path("/A/B/C").anchor
        self.assertEqual(excpected, actual)

    def test_suffix(self):
        excpected = ".bak"
        actual = Path("file.txt.bak").suffix
        self.assertEqual(excpected, actual)

    def test_ext(self):
        excpected = ".bak"
        actual = Path("file.txt.bak").ext
        self.assertEqual(excpected, actual)

    def test_suffixes(self):
        excpected = [".txt", ".bak"]
        actual = Path("file.txt.bak").suffixes
        self.assertEqual(excpected, actual)

    def test_home(self):
        excpected = Path("B")
        actual = Path("/A/B/C").relpath("/A").home
        self.assertEqual(excpected, actual)
        self.assertEqual(excpected.abspath(), actual.abspath())
        self.typed_instance_test(actual)

    def test_home_root(self):
        excpected = Path("")
        actual = Path("/").home
        self.assertEqual(excpected, actual)
        self.assertEqual(excpected.abspath(), actual.abspath())
        self.typed_instance_test(actual)

    def test_hash(self):
        with self.assertWarns(SyntaxWarning):
            expected = hash(Path("/A") / "B")
        with self.assertWarns(SyntaxWarning):
            actual = hash(Path("/A/B/"))
        self.assertEqual(expected, actual)

    def test_lt_gt_last(self):
        lesser = Path("/A/B/")
        lesser2 = Path("/A/B")
        greater = Path("/A/C")
        # lt gt
        self.assertFalse(lesser < lesser2)
        self.assertFalse(lesser > lesser2)
        self.assertLess(lesser, greater)
        self.assertGreater(greater, lesser)
        # le ge
        self.assertLessEqual(lesser, lesser2)
        self.assertGreaterEqual(lesser, lesser2)
        self.assertLessEqual(lesser, greater)
        self.assertGreaterEqual(greater, lesser)

    def test_lt_gt_le_ge_first(self):
        lesser = Path("/A/D")
        lesser2 = Path("/A/D/")
        greater = Path("/B/C")
        # lt gt
        self.assertFalse(lesser < lesser2)
        self.assertFalse(lesser > lesser2)
        self.assertLess(lesser, greater)
        self.assertGreater(greater, lesser)
        # le ge
        self.assertLessEqual(lesser, lesser2)
        self.assertGreaterEqual(lesser, lesser2)
        self.assertLessEqual(lesser, greater)
        self.assertGreaterEqual(greater, lesser)

    def test_sort(self):
        first = Path("/A/B/C")
        second = Path("/A/C")
        third = Path("/B/A/A")
        expected = [first, second, third]
        actual = sorted([third, first, second])
        self.assertEqual(expected, actual)

    def test_lt_gt_le_ge_str(self):
        path = Path("/A/B/")
        greater = "/A/C"
        lesser = "/A/A"
        equal = "/A/B"
        self.assertGreater(path, lesser)
        self.assertGreaterEqual(path, lesser)
        self.assertLess(path, greater)
        self.assertLessEqual(path, greater)
        self.assertLessEqual(path, equal)
        self.assertLessEqual(path, greater)
        self.assertGreaterEqual(path, equal)
        self.assertGreaterEqual(path, lesser)

    def test_getitem(self):
        expected = "A"
        actual_root = Path("/A/B/")[1]
        actual_name = Path("/B/A/").name[0]
        self.assertEqual(expected, actual_root)
        self.assertEqual(expected, actual_name)

    def test_static_posix_string(self):
        expected = "/A/B/C"
        actual = Path.posix_string(Path("\\A\\B/C"))
        self.assertEqual(expected, actual)

    def test_posix_string(self):
        expected = "/A/B/C"
        actual = Path("\\A\\B/C", posix=False).posix_string()
        actual2 = Path("/A\\B\\C", posix=True).posix_string()
        self.assertEqual(expected, actual)
        self.assertEqual(expected, actual2)

    def test_posix_enabled(self):
        enabled = Path("/A/B", posix=True).posix_enabled
        disabled = Path("/A/B", posix=False).posix_enabled
        disabled2 = Path("/A/B").posix_enabled
        self.assertTrue(enabled)
        self.assertFalse(disabled)
        self.assertFalse(disabled2)

    def test_cwd(self):
        start = Path("/A/B/")
        self.assertEqual(start.cwd, Path.getcwd())
