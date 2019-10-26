import os
import time
from types import GeneratorType
from typing import List

from mutapath import Path
from mutapath.exceptions import PathException
from tests.helper import PathTest, file_test


class TestWithPath(PathTest):
    def __init__(self, *args):
        self.test_path = "with_path_test"
        super().__init__(*args)

    @file_test(equal=False)
    def test_wrapped_list(self, test_file: Path):
        """Verify that nested functions returning lists have been mapped to the correct types"""
        expected = [test_file]
        actual = self.test_base.listdir()
        self.assertEqual(expected, actual)
        self.typed_instance_test(actual[0])
        self.assertIsInstance(actual, List)

    @file_test(equal=False)
    def test_wrapped_generator(self, test_file: Path):
        """Verify that nested generators have been mapped to the correct types"""
        expected = [test_file]
        actual = self.test_base.walk()
        actual_list = list(actual)
        self.assertEqual(expected, actual_list)
        self.typed_instance_test(actual_list[0])
        self.assertIsInstance(actual, GeneratorType)

    @file_test(equal=False)
    def test_glob(self, test_file: Path):
        """Verify that glob is returning the correct types"""
        expected = [test_file]
        actual = self.test_base.glob("*.file")
        actual_list = list(actual)
        self.assertEqual(expected, actual_list)
        self.typed_instance_test(actual_list[0])
        self.assertIsInstance(actual, GeneratorType)

    @file_test(equal=False)
    def test_rglob(self, test_file: Path):
        """Verify that rglob (which is fetched from pathlib.Path) is returning the correct types"""
        expected = [test_file]
        actual = self.test_base.rglob("*.file")
        actual_list = list(actual)
        self.assertEqual(expected, actual_list)
        self.typed_instance_test(actual_list[0])
        self.assertIsInstance(actual, GeneratorType)

    @file_test(equal=False)
    def test_open(self, test_file: Path):
        expected = "test"
        with test_file.open("w") as w:
            w.write(expected)
        actual = test_file.read_text()
        self.assertEqual(expected, actual)

    @file_test(equal=False)
    def test_size(self, test_file: Path):
        expected = 0
        actual = test_file.size
        self.assertEqual(expected, actual)

    @file_test(equal=False)
    def test_mtime(self, test_file: Path):
        actual = test_file.mtime
        time.sleep(0.1)
        other = test_file.with_name("other.txt").touch()
        later = other.mtime
        self.assertGreater(later, actual)
        test_file.copystat(other)
        later = other.mtime
        self.assertEqual(later, actual)

    @file_test(equal=False)
    def test_ctime(self, test_file: Path):
        actual = test_file.ctime
        time.sleep(0.1)
        other = test_file.with_name("other.txt").touch()
        later = other.ctime
        self.assertGreater(later, actual)

    @file_test(equal=False)
    def test_atime(self, test_file: Path):
        actual = test_file.atime
        other = test_file.copy2(test_file.with_name("other.txt"))
        later = other.atime
        self.assertEqual(later, actual)

    @file_test(exists=False)
    def test_mutate(self, test_file: Path):
        expected = test_file.with_name("new.txt")
        with test_file.mutate() as mut:
            mut.suffix = ".txt"
            mut.stem = "new"
        return expected

    @file_test()
    def test_rename_in_mutate(self, test_file: Path):
        """Try to rename a file in mutate"""
        expected = test_file.with_name("new.txt")
        with test_file.mutate() as mut:
            mut.rename(expected)
        return expected

    @file_test()
    def test_renaming(self, test_file: Path):
        """Try renaming a file without issues"""
        expected = test_file.with_name("new.txt")
        with test_file.renaming() as mut:
            mut.stem = "new"
            mut.suffix = ".txt"
        return expected

    @file_test()
    def test_renaming_with_renames(self, test_file: Path):
        """Try renaming a file with another os method"""
        expected = test_file.with_name("new.txt")
        with test_file.renaming(method=os.renames) as mut:
            mut.stem = "new"
            mut.suffix = ".txt"
        return expected

    @file_test()
    def test_renaming_fail(self, test_file: Path):
        """Try renaming when the target file already exists"""
        expected = test_file.normpath()
        wrong = test_file.with_name("new.txt")
        test_file.copy(wrong)
        with self.assertRaises(PathException):
            with test_file.renaming() as mut:
                mut.name = wrong.name
        return expected

    @file_test(exists=False)
    def test_renaming_source_missing(self, test_file: Path):
        """Try renaming when the source file is missing"""
        with test_file.mutate() as mut:
            mut.name = "wrong.txt"
        expected = ~ test_file
        with self.assertRaises(PathException):
            with test_file.renaming() as mut:
                mut.name = expected.name
        return expected

    @file_test()
    def test_renaming_source_lock_fail(self, test_file: Path):
        """Try renaming when there is already a lock on the source file"""
        expected = ~ test_file
        anything = test_file.with_name("anything.txt")
        with expected.lock:
            with self.assertRaises(PathException):
                with test_file.renaming(timeout=0.1) as mut:
                    mut.name = anything.name
        return expected

    @file_test()
    def test_renaming_without_lock(self, test_file: Path):
        """Try renaming when lock=False even though there is already a lock on the source and the target file"""
        expected = ~ test_file
        target = test_file.with_name("target.txt").touch()
        with expected.lock:
            with target.lock:
                target.remove()
                with test_file.renaming(lock=False) as mut:
                    mut.name = target.name
        return target

    @file_test()
    def test_renaming_target_lock_fail(self, test_file: Path):
        """Try renaming to a path for which there is already a lock but not a file itself"""
        expected = ~ test_file
        target = test_file.with_name("target.txt").touch()
        with target.lock:
            target.remove()
            with self.assertRaises(PathException):
                with test_file.renaming(timeout=0.1) as mut:
                    mut.name = target.name
        return expected

    @file_test()
    def test_copying(self, test_file: Path):
        """Try copying a file without issues"""
        expected = test_file.with_name("new.txt")
        with test_file.copying() as mut:
            mut.stem = "new"
            mut.suffix = ".txt"
        self.assertEqual(expected.read_text(), test_file.read_text())
        return expected

    @file_test(equal=False, instance=False, exists=False)
    def test_moving(self, test_file: Path):
        """Try moving a file without issues"""
        expected = self.test_base / "to"
        from_here = self.test_base / "from/here"
        from_here.makedirs()
        test_file.copy(from_here)
        with from_here.moving() as mut:
            mut.joinpath(self.test_base, "to")
        self.assertEqual(expected, from_here)
        self.assertIsInstance(from_here, Path)
        self.assertTrue(from_here.exists(), "File has to exist")

    @file_test(equal=False)
    def test_text(self, test_file: Path):
        expected = "test"
        with test_file.open("w") as w:
            w.write(expected)
        actual = test_file.text
        actual2 = test_file.read_text()
        self.assertEqual(expected, actual)
        self.assertEqual(expected, actual2)
        with test_file.open("w") as w:
            w.write("test2")
        updated = test_file.text
        updated2 = test_file.read_text()
        self.assertEqual(expected, updated)
        self.assertNotEqual(expected, updated2)

    @file_test(equal=False)
    def test_bytes(self, test_file: Path):
        with test_file.open("w") as w:
            w.write("test")
        expected = test_file.read_bytes()
        actual = test_file.bytes
        self.assertEqual(expected, actual)
