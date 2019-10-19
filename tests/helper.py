import unittest
from functools import wraps

import path

from mutapath import Path


def file_test(equal: bool = True, instance: bool = True, exists: bool = True, posix_test: bool = True):
    def file_test_decorator(func):
        @wraps(func)
        def func_wrapper(cls: PathTest):
            def test_case(use_posix: bool = False) -> Path:
                actual = cls._gen_start_path(use_posix)
                expected = func(cls, actual)
                if equal:
                    cls.assertIsNotNone(expected, "This test does not return the expected value. Fix the test.")
                    cls.assertEqual(expected, actual)
                if instance:
                    cls.typed_instance_test(actual)
                if exists:
                    cls.assertTrue(actual.exists(), "The tested file does not exist.")
                return actual

            try:
                test_case()
                if posix_test:
                    test_path = test_case(use_posix=True)
                    cls.assertTrue(test_path.posix_enabled, "the test file is not in posix format")
            finally:
                cls._clean()

        return func_wrapper

    return file_test_decorator


class PathTest(unittest.TestCase):
    test_path = "test_path"

    def __init__(self, *args):
        super().__init__(*args)

    def _gen_start_path(self, posix: bool = False):
        self.test_base = Path.getcwd() / self.test_path
        self.test_base.rmtree_p()
        self.test_base.mkdir()
        new_file = self.test_base / "test.file"
        new_file.touch()
        return new_file.with_poxis_enabled(posix)

    def _clean(self):
        self.test_base.rmtree_p()

    def typed_instance_test(self, instance):
        self.assertIsInstance(instance, Path)
        self.assertIsInstance(instance._contained, path.Path)
