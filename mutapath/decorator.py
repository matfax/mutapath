"""
The decorators convert all returning types to mutapath.Path, or mutapath.MutaPath instances, respectively.
The following types are covered:
* Internal routines returning non-iterable types in mutapath
* All types returned from routines and properties from pathlib
* All types returned from routines and properties from path
"""
import functools
import inspect
import pathlib
from typing import List, Iterable, Callable, Optional

import path

import mutapath

__EXCLUDE_FROM_WRAPPING = [
    "__dir__", "__eq__", "__format__", "__repr__", "__str__", "__sizeof__", "__init__", "__getattribute__",
    "__delattr__", "__setattr__", "__getattr__", "joinpath", "clone", "__exit__", "__fspath__",
    "'_Path__wrap_attribute'", "__wrap_decorator", "_op_context", "__hash__", "__enter__", "_norm", "open", "lock",
    "getcwd", "dirname", "owner", "uncshare", "posix_format", "posix_string", "__add__", "__radd__", "_set_contained",
    "with_poxis_enabled", "_hash_cache", "_serialize", "_deserialize", "string_repr_enabled", "_shorten_duplicates"
]

__MUTABLE_FUNCTIONS = {"rename", "renames", "copy", "copy2", "copyfile", "copymode", "copystat", "copytree", "move",
                       "basename", "abspath", "join", "joinpath", "normpath", "relpath", "realpath", "relpathto"}


def __is_mbm(member):
    if isinstance(member, property):
        return True
    return __is_def(member)


def __is_def(member):
    while isinstance(member, functools.partial):
        member = member.func
    if inspect.isbuiltin(member):
        return False
    return inspect.isroutine(member)


def __path_converter(const: Callable):
    def convert_path(result):
        if isinstance(result, (path.Path, pathlib.PurePath)):
            return const(result)
        return result

    return convert_path


def __path_func(orig_func):
    @functools.wraps(orig_func)
    def wrap_decorator(cls, *args, **kwargs):
        result = orig_func(cls, *args, **kwargs)
        return __path_converter(cls.clone)(result)

    return wrap_decorator


def wrap_attribute(orig_attr, fetcher: Optional[Callable] = None):
    @functools.wraps(orig_attr)
    def __wrap_decorator(self, *args, **kwargs):
        fetched = self._contained
        if fetcher is not None:
            fetched = fetcher(fetched)

        if isinstance(orig_attr, property):
            result = orig_attr.__get__(fetched)
        else:
            result = orig_attr(fetched, *args, **kwargs)

        if result is None:
            return None

        converter = __path_converter(self.clone)
        if isinstance(result, List) and not isinstance(result, (str, bytes, bytearray)):
            return list(map(converter, result))
        if isinstance(result, Iterable) and not isinstance(result, (str, bytes, bytearray)):
            return (converter(g) for g in result)
        return __path_converter(self.clone)(result)

    if isinstance(orig_attr, property):
        return property(fget=__wrap_decorator, doc=orig_attr.__doc__)

    return __wrap_decorator


def path_wrapper(cls):
    member_names = list()
    for name, method in inspect.getmembers(cls, __is_def):
        if name not in __EXCLUDE_FROM_WRAPPING:
            setattr(cls, name, __path_func(method))
            member_names.append(name)
    for name, _ in inspect.getmembers(path.Path, __is_mbm):
        if not name.startswith("_") \
                and name not in __EXCLUDE_FROM_WRAPPING \
                and name not in member_names:
            method = getattr(path.Path, name)
            if not hasattr(cls, name):
                setattr(cls, name, wrap_attribute(method))
                member_names.append(name)
    for name, _ in inspect.getmembers(pathlib.Path, __is_mbm):
        if not name.startswith("_") \
                and name not in __EXCLUDE_FROM_WRAPPING \
                and name not in member_names:
            method = getattr(pathlib.Path, name)
            if not hasattr(cls, name):
                setattr(cls, name, wrap_attribute(method, pathlib.Path))
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
            if isinstance(result, mutapath.Path):
                self._contained = result._contained
                return self
            return result

        result = orig_func(self, *args, **kwargs)
        return cls(result)

    return mutation_decorator


def mutable_path_wrapper(cls):
    names, _ = zip(*inspect.getmembers(path.Path, __is_def))
    names = __MUTABLE_FUNCTIONS.intersection(names)
    for method_name in names:
        setattr(cls, method_name, __mutate_func(cls, method_name))
    return cls
