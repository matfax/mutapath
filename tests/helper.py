import unittest
from functools import wraps
from typing import Callable, Optional

import path

from mutapath import Path


class PathTest(unittest.TestCase):
    test_path = "test_path"

    def __init__(self, *args):
        super().__init__(*args)

    def _gen_start_path(self, posix: bool = False, string_repr: bool = False):
        self.test_base = Path.getcwd() / self.test_path
        self.test_base.rmtree_p()
        self.test_base.mkdir()
        new_file = self.test_base / "test.file"
        new_file.touch()
        with_string_repr = Path(new_file, string_repr=string_repr)
        return with_string_repr.with_poxis_enabled(posix)

    def _clean(self):
        self.test_base.rmtree_p()

    def typed_instance_test(self, *instance):
        for i in instance:
            self.assertIsInstance(i, Path)
            self.assertIsInstance(i._contained, path.Path)

    def arg_with_matrix(self, with_func: Callable[[Path, bool], Path],
                        test_func: Optional[Callable[[Path], bool]] = None,
                        with_func_default: bool = True, **kwargs):
        """
        Use a matrix of keyed init arguments with their immutable with methods.
        The first passed keyed argument should relate to the with method.
        """
        if len(kwargs) < 1:
            raise ValueError(
                "The matrix requires at least the init value and its default that correlates with the with method.")

        first_key = next(iter(kwargs))
        first_default = kwargs[first_key]
        remaining_kwargs = kwargs.copy()
        del remaining_kwargs[first_key]
        enabled_kwarg = dict()
        enabled_kwarg[first_key] = True
        disabled_kwarg = dict()
        disabled_kwarg[first_key] = False

        default_path = Path("/A/B/other.txt", **remaining_kwargs)
        enabled = Path("/A/B/other.txt", **enabled_kwarg, **remaining_kwargs)
        disabled = Path("/A/B/other.txt", **disabled_kwarg, **remaining_kwargs)

        for path in default_path, enabled, disabled:

            default_case = with_func(path)
            with_enabled = with_func(path, True)
            with_disabled = with_func(path, False)
            if with_func_default:
                self.assertEqual(enabled, default_case)
            else:
                self.assertEqual(disabled, default_case)
            self.assertEqual(enabled, with_enabled)
            self.assertEqual(disabled, with_disabled)
            self.typed_instance_test(default_case, with_enabled, with_disabled)
            if test_func is not None:
                self.assertEqual(first_default, test_func(default_path))
                self.assertTrue(test_func(enabled))
                self.assertFalse(test_func(disabled))
                self.assertTrue(test_func(with_enabled))
                self.assertFalse(test_func(with_disabled))
                self.assertTrue(test_func(with_enabled.clone("/")))
                self.assertFalse(test_func(with_disabled.clone("/")))


def file_test(equal=True, instance=True, exists=True, posix_test=True, string_test=True):
    def file_test_decorator(func):
        @wraps(func)
        def func_wrapper(cls: PathTest):
            def test_case(use_posix: bool = False, use_string: bool = False) -> Path:
                actual = cls._gen_start_path(use_posix, use_string)
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
                if string_test:
                    test_path = test_case(use_string=True)
                    cls.assertTrue(test_path.string_repr_enabled, "the test file is not using string representation")
            finally:
                cls._clean()

        return func_wrapper

    return file_test_decorator
