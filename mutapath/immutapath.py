import os
import pathlib
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Union, Iterable, ClassVar, Callable

import path

import mutapath
from mutapath.decorator import path_wrap
from mutapath.exceptions import PathException


@path_wrap
@dataclass(repr=False, eq=False)
class Path(object):
    """Immutable Path"""
    __mutable: ClassVar[object]
    _contained: Union[path.Path, pathlib.Path, str] = ""

    def __post_init__(self):
        if isinstance(self._contained, path.Path):
            normalized = self._norm(self._contained)
            if not self._contained == normalized:
                self._contained = normalized
        else:
            if isinstance(self._contained, str):
                self._contained = path.Path(self._contained)
            if isinstance(self._contained, Path):
                self._contained = self._contained._contained
            if isinstance(self._contained, pathlib.Path):
                self._contained = path.Path(str(self._contained))

    def __dir__(self) -> Iterable[str]:
        return sorted(super(Path, self).__dir__()) + dir(path.Path)

    def __getattr__(self, item):
        return getattr(self._contained, item)

    def __setattr__(self, key, value):
        if key == "_contained":
            if isinstance(value, Path):
                value = value._contained
            super(Path, self).__setattr__(key, value)
            self.__post_init__()
        elif key == "_Path__mutable":
            super(Path, self).__setattr__(key, value)
        else:
            raise AttributeError("mutapath.Path is an immutable class, unless mutate() context is used.")

    def __repr__(self):
        return repr(self._contained)

    def __str__(self):
        return self._contained

    def __eq__(self, other):
        if isinstance(other, Path):
            return self._contained == other._contained
        if isinstance(other, path.Path):
            return self._contained == self._norm(other)
        if isinstance(other, pathlib.Path):
            return self._contained == Path(other)._contained
        if isinstance(other, str):
            return str(self) == str(other)
        return super(Path, self).__eq__(other)

    def __add__(self, other):
        return self._contained.__add__(Path(other)._contained)

    def __radd__(self, other):
        return self._contained.__radd__(Path(other)._contained)

    def __div__(self, other):
        return self._contained.__div__(Path(other)._contained)

    __truediv__ = __div__

    def __rdiv__(self, other):
        return self._contained.__rdiv__(Path(other)._contained)

    __rtruediv__ = __rdiv__

    def __enter__(self):
        return self._contained.__enter__()

    def __exit__(self, *_):
        return self._contained.__exit__()

    def __fspath__(self):
        return self._contained.__fspath__()

    def __invert__(self):
        """Create a MutaPath from immutable Path"""
        from mutapath import MutaPath
        return MutaPath(self._contained)

    @staticmethod
    def _norm(pathly: path.Path):
        return path.Path(path.Path.module.normpath(pathly))

    def with_name(self, new_name):
        """
        Clone this path with a new name

        .. seealso:: :func:`pathlib.Path.with_name`
        """
        return self.base.joinpath(str(new_name))

    def with_stem(self, new_stem):
        """Clone this path with a new stem"""
        return self.base.joinpath(str(new_stem)).with_suffix(self.ext)

    def with_parent(self, new_parent):
        """Clone this path with a new parent"""
        return Path(new_parent).joinpath(str(self.name))

    def with_base(self, base, strip_length: int = 0):
        """
        Clone this path with a new base.

        The given path is used in its full length as base of this path, if strip_length is not specified.
        If strip_length is specified, the given number of path elements are stripped from the left side,
        and the given base is prepended.

        >>> Path('/home/doe/folder/sub').with_base("/home/joe")
        Path('/home/joe/folder/sub')

        >>> Path('/home/doe/folder/sub').with_base("/home/joe", strip_length=1)
        Path('/home/joe/doe/folder/sub')

        """
        base = Path(base)
        if not strip_length:
            strip_length = len(base.splitall())
        else:
            strip_length += 1

        if len(self.splitall()) <= strip_length:
            raise ValueError("The given base has more elements than this path.")
        stripped = Path.joinpath(*self.splitall()[strip_length:])
        return base.joinpath(stripped)

    @classmethod
    def getcwd(cls):
        return Path(os.getcwd())

    @path.multimethod
    def joinpath(self, first, *others):
        contained_others = map(str, list(others))
        joined = path.Path.joinpath(self._contained, str(first), *contained_others)
        return Path(joined)

    @property
    def suffix(self):
        """Get file suffix"""
        return self.ext

    @suffix.setter
    def suffix(self, value):
        """Set file suffix"""
        self._contained = self.with_suffix(value)

    @property
    def ext(self):
        """Get file name"""
        return Path(self._contained.ext)

    @property
    def name(self):
        """Get file name"""
        return Path(self._contained.name)

    @name.setter
    def name(self, value):
        """Set file name"""
        self._contained = self.with_name(value)

    @property
    def base(self):
        """
        Get path base (i.e., the parent of the file)

        seealso:: :func:`pathlib.Path.parent`
        """
        return Path(self._contained.parent)

    @base.setter
    def base(self, value):
        """
        Set a new file base

        seealso:: :func:`mutapath.Path.with_base`
        """
        self._contained = self.with_base(value)

    @property
    def uncshare(self):
        """
        Get this path as UNC mount point

        seealso:: :func:`pathlib.Path.uncshare`
        """
        return Path(self._contained.uncshare)

    @property
    def stem(self):
        """
        Get path stem

        seealso:: :func:`pathlib.Path.stem`
        """
        return Path(self._contained.stem)

    @stem.setter
    def stem(self, value):
        """
        Set a new file stem

        seealso:: :func:`mutapath.Path.with_stem`
        """
        self._contained = self.with_stem(value)

    @property
    def drive(self):
        """
        Get path drive

        seealso:: :func:`pathlib.Path.drive`
        """
        return Path(self._contained.drive)

    @property
    def parent(self):
        """
        Get the parent path

        seealso:: :func:`pathlib.Path.parent`
        """
        return Path(self._contained.parent)

    @parent.setter
    def parent(self, value):
        """
        Set a new file parent

        seealso:: :func:`mutapath.Path.with_parent`
        """
        self._contained = self.with_parent(value)

    @property
    def parents(self):
        """
        Get a list of all parent paths

        seealso:: :func:`pathlib.Path.parents`
        """
        result = pathlib.Path(self._contained).parents
        return map(Path, result)

    @property
    def dirname(self):
        """
        Get the parent path

        seealso:: :func:`pathlib.Path.dirname`
        """
        return Path(self._contained.dirname())

    @contextmanager
    def mutate(self):
        """
        Create a mutable context for this immutable path.

        >>> with Path('/home/doe/folder/sub').mutate() as mut:
        ...     mut.name = "top"
        Path('/home/doe/folder/top')

        """
        self.__mutable = mutapath.MutaPath(self)
        yield self.__mutable
        self._contained = getattr(self.__mutable, "_contained")

    @contextmanager
    def _op_context(self, name: str, op: Callable):
        self.__mutable = mutapath.MutaPath(self)
        yield self.__mutable
        current_file = self._contained
        target_file = getattr(self.__mutable, "_contained")
        try:
            current_file = op(current_file, target_file)
        except FileExistsError as e:
            raise PathException(
                f"{name.capitalize()} to {current_file.normpath()} failed because the file already exists. "
                                f"Falling back to original value {self._contained}.") from e
        else:
            if not current_file.exists():
                raise PathException(
                    f"{name.capitalize()} to {current_file.normpath()} failed because can not be found. "
                                    f"Falling back to original value {self._contained}.")

        self._contained = current_file

    def renaming(self):
        """
        Create a renaming context for this immutable path.
        The external value is only changed if the renaming succeeds.

        >>> with Path('/home/doe/folder/a.txt').renaming() as mut:
        ...     mut.stem = "b"
        Path('/home/doe/folder/b.txt')

        """

        def checked_rename(cls: path.Path, target: path.Path):
            if target.exists():
                raise FileExistsError(f"{target.name} already exists.")
            else:
                return cls.rename(target)

        return self._op_context("Renaming", checked_rename)

    def moving(self):
        """
        Create a moving context for this immutable path.
        The external value is only changed if the moving succeeds.

        >>> with Path('/home/doe/folder/a.txt').moving() as mut:
        ...     mut.stem = "b"
        Path('/home/doe/folder/b.txt')

        """
        return self._op_context("Moving", path.Path.move)

    def copying(self):
        """
        Create a copying context for this immutable path.
        The external value is only changed if the copying succeeds.

        >>> with Path('/home/doe/folder/a.txt').copying() as mut:
        ...     mut.stem = "b"
        Path('/home/doe/folder/b.txt')

        """
        return self._op_context("Copying", path.Path.copy)
