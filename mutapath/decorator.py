import functools
import inspect
from types import GeneratorType
from typing import List, Iterable, Callable

import path

import mutapath

__EXCLUDE_FROM_WRAPPING = [
    "__dir__", "__eq__", "__format__", "__repr__", "__str__", "__sizeof__", "__init__", "__getattribute__",
    "__delattr__", "__setattr__", "__getattr__", "joinpath", "clone", "__exit__", "__fspath__",
    "'_Path__wrap_attribute'", "__wrap_decorator", "_op_context", "__hash__", "__enter__", "_norm", "open", "lock",
    "getcwd", "dirname", "owner", "uncshare", "posix_format", "posix_string", "__add__", "__radd__", "_set_contained",
    "with_poxis_enabled"
]

__MUTABLE_FUNCTIONS = {"rename", "renames", "copy", "copy2", "copyfile", "copymode", "copystat", "copytree", "move",
                       "basename", "abspath", "join", "joinpath", "normpath", "relpath", "realpath", "relpathto"}


def __is_def(member):
    while isinstance(member, functools.partial):
        member = member.func
    if inspect.isbuiltin(member):
        return False
    return inspect.isroutine(member)


def __path_converter(const: Callable):
    def convert_path(result):
        if isinstance(result, path.Path):
            return const(result)
        return result

    return convert_path


def __path_func(orig_func):
    @functools.wraps(orig_func)
    def wrap_decorator(cls, *args, **kwargs):
        result = orig_func(cls, *args, **kwargs)
        return __path_converter(cls.clone)(result)

    return wrap_decorator


def wrap_attribute(orig_func):
    @functools.wraps(orig_func)
    def __wrap_decorator(cls, *args, **kwargs):
        result = orig_func(cls._contained, *args, **kwargs)
        if isinstance(result, List) and not isinstance(result, str):
            return list(map(__path_converter(cls.clone), result))
        if isinstance(result, Iterable) and not isinstance(result, str):
            return iter(map(__path_converter(cls.clone), result))
        if isinstance(result, GeneratorType):
            return map(__path_converter(cls.clone), result)
        return __path_converter(cls.clone)(result)

    return __wrap_decorator


def path_wrapper(cls):
    members = inspect.getmembers(cls, __is_def)
    for name, method in members:
        if name not in __EXCLUDE_FROM_WRAPPING:
            setattr(cls, name, __path_func(method))
    member_names, _ = zip(*members)
    for name, _ in inspect.getmembers(path.Path, __is_def):
        if not name.startswith("_") \
                and name not in __EXCLUDE_FROM_WRAPPING \
                and name not in member_names:
            method = getattr(path.Path, name)
            assert not hasattr(cls, name)
            setattr(cls, name, wrap_attribute(method))
    return cls


def __mutate_func(cls, method_name):
    orig_func = getattr(path.Path, method_name)

    @functools.wraps(orig_func)
    def mutation_decorator(self, *args, **kwargs):
        if isinstance(self, mutapath.Path):
            result = orig_func(self._contained, *args, **kwargs)
            if isinstance(result, path.Path):
                self._contained = result
                return self
            elif isinstance(result, mutapath.Path):
                self._contained = result._contained
                return self
            return result
        else:
            result = orig_func(self, *args, **kwargs)
            return cls(result)

    return mutation_decorator


def mutable_path_wrapper(cls):
    names, _ = zip(*inspect.getmembers(path.Path, __is_def))
    names = __MUTABLE_FUNCTIONS.intersection(names)
    for method_name in names:
        setattr(cls, method_name, __mutate_func(cls, method_name))
    return cls
