import functools
import inspect

import path

import mutapath

__EXCLUDE_FROM_WRAPPING = ["__dir__", "__eq__", "__format__", "__repr__", "__str__", "__sizeof__", "__init__",
                           "__post_init__", "__getattribute__", "__delattr__", "__setattr__", "__getattr__",
                           "__fspath__", "_norm"]

__MUTABLE_FUNCTIONS = {"rename", "renames", "copy", "copy2", "copyfile", "copymode", "copystat", "copytree", "move",
                       "basename", "abspath", "join", "joinpath", "normpath", "relpath", "realpath", "relpathto"}


def __is_def(member):
    while isinstance(member, functools.partial):
        member = member.func
    if inspect.isbuiltin(member):
        return False
    return inspect.isroutine(member)


def __path_func(orig_func):
    def wrap_decorator(*args, **kwargs):
        result = orig_func(*args, **kwargs)
        if isinstance(result, path.Path):
            return mutapath.Path(result)
        else:
            return result

    return wrap_decorator


def path_wrap(cls):
    for name, method in inspect.getmembers(path.Path, __is_def):
        if not name.startswith("__"):
            setattr(path.Path, name, __path_func(method))
    for name, method in inspect.getmembers(cls, __is_def):
        if name not in __EXCLUDE_FROM_WRAPPING:
            setattr(cls, name, __path_func(method))
    return cls


def __mutate_func(cls, method_name):
    from mutapath import Path

    def mutation_decorator(self, *args, **kwargs):
        orig_func = getattr(path.Path, method_name)
        if isinstance(self, Path):
            result = orig_func(self._contained, *args, **kwargs)
            if isinstance(result, mutapath.Path):
                self._contained = result._contained
                return self
            else:
                return result
        else:
            result = orig_func(self, *args, **kwargs)
            return cls(result)

    return mutation_decorator


def path_mutable(cls):
    names, _ = zip(*inspect.getmembers(path.Path, __is_def))
    names = __MUTABLE_FUNCTIONS.intersection(names)
    for method_name in names:
        setattr(cls, method_name, __mutate_func(cls, method_name))
    return cls
