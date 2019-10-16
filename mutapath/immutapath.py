from __future__ import annotations

import contextlib
import io
import os
import pathlib
import shutil
from contextlib import contextmanager
from dataclasses import dataclass
from types import GeneratorType
from typing import Union, Iterable, ClassVar, Callable, List
from xml.dom.minicompat import StringTypes

import filelock
import path
from cached_property import cached_property
from filelock import SoftFileLock

import mutapath
from mutapath.decorator import path_wrap, _convert_path
from mutapath.exceptions import PathException
from mutapath.lock_dummy import DummyFileLock


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

    @staticmethod
    def __wrap_attribute(orig_func):
        def __wrap_decorator(*args, **kwargs):
            result = orig_func(*args, **kwargs)
            if isinstance(result, List) and not isinstance(result, StringTypes):
                return list(map(_convert_path, result))
            if isinstance(result, Iterable) and not isinstance(result, StringTypes):
                return iter(map(_convert_path, result))
            if isinstance(result, GeneratorType):
                return map(_convert_path, result)
            return _convert_path(result)

        return __wrap_decorator

    def __getattr__(self, item):
        attr = getattr(self._contained, item)
        return Path.__wrap_attribute(attr)

    def __setattr__(self, key, value):
        if key == "_contained":
            lock = self.__dict__.get("lock", None)
            if lock is not None:
                if self.lock.is_locked:
                    self.lock.release()
                    Path(self.lock.lock_file).remove_p()
                del self.__dict__['lock']

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

    def __hash__(self):
        return hash(self._contained)

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

    def __lt__(self, other):
        if isinstance(other, Path):
            return self.splitall() < other.splitall()
        left = str(self).replace("\\\\", "\\").replace("\\", "/")
        right = str(other).replace("\\\\", "\\").replace("\\", "/")
        return left < right

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
        return Path(self._contained.__enter__())

    def __exit__(self, *_):
        self._contained.__exit__()

    def __fspath__(self):
        return self._contained.__fspath__()

    def __invert__(self):
        """Create a MutaPath from immutable Path"""
        from mutapath import MutaPath
        return MutaPath(self._contained)

    @staticmethod
    def _norm(pathly: path.Path):
        return path.Path(path.Path.module.normpath(pathly))

    def with_name(self, new_name) -> Path:
        """
        Clone this path with a new name

        .. seealso:: :func:`pathlib.Path.with_name`
        """
        return self.base.joinpath(str(new_name))

    def with_stem(self, new_stem) -> Path:
        """Clone this path with a new stem"""
        return self.base.joinpath(str(new_stem)).with_suffix(self.ext)

    def with_parent(self, new_parent) -> Path:
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
    def getcwd(cls) -> Path:
        return Path(os.getcwd())

    @path.multimethod
    def joinpath(self, first, *others) -> Path:
        contained_others = map(str, others)
        joined = path.Path.joinpath(self._contained, str(first), *contained_others)
        return Path(joined)

    @property
    def home(self) -> Path:
        """
        Get the home path of the current path representation.

        >>> Path("/home/doe/folder/sub").home
        Path("home")

        :return: the home path
        """
        split = self.splitall()
        if len(split) <= 1:
            return self.drive
        for parent in self.parents:
            if parent.name == split[1]:
                return parent.name
        return self.drive

    @property
    def suffix(self) -> str:
        """Get file suffix"""
        return self.ext

    @suffix.setter
    def suffix(self, value):
        """Set file suffix"""
        self._contained = self.with_suffix(value)

    @property
    def ext(self) -> str:
        """Get file name"""
        return self._contained.ext

    @property
    def name(self) -> Path:
        """Get file name"""
        return Path(self._contained.name)

    @name.setter
    def name(self, value):
        """Set file name"""
        self._contained = self.with_name(value)

    @property
    def base(self) -> Path:
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
    def uncshare(self) -> Path:
        """
        Get this path as UNC mount point

        seealso:: :func:`pathlib.Path.uncshare`
        """
        return Path(self._contained.uncshare)

    @property
    def stem(self) -> str:
        """
        Get path stem

        seealso:: :func:`pathlib.Path.stem`
        """
        return self._contained.stem

    @stem.setter
    def stem(self, value):
        """
        Set a new file stem

        seealso:: :func:`mutapath.Path.with_stem`
        """
        self._contained = self.with_stem(value)

    @property
    def drive(self) -> Path:
        """
        Get path drive

        seealso:: :func:`pathlib.Path.drive`
        """
        return Path(self._contained.drive)

    @property
    def parent(self) -> Path:
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
    def parents(self) -> Iterable[Path]:
        """
        Get a list of all parent paths

        seealso:: :func:`pathlib.Path.parents`
        """
        result = pathlib.Path(self._contained).parents
        return iter(map(Path, result))

    @property
    def dirname(self) -> Path:
        """
        Get the parent path

        seealso:: :func:`pathlib.Path.dirname`
        """
        return Path(self._contained.dirname())

    @property
    def size(self) -> int:
        """
        Get the size of the file

        seealso:: :func:`path.Path.size`
        """
        return self._contained.size

    @property
    def ctime(self) -> float:
        """
        Get the creation time of the file

        seealso:: :func:`os.path.getctime`
        """
        return self._contained.ctime

    @property
    def mtime(self) -> float:
        """
        Get the mtime of the file

        seealso:: :func:`os.path.getmtime`
        """
        return self._contained.mtime

    @property
    def atime(self) -> float:
        """
        Get the atime of the file

        seealso:: :func:`os.path.getatime`
        """
        return self._contained.atime

    @property
    def owner(self):
        """
        Get the owner of the file.
        """
        return self._contained.owner

    def open(self, *args, **kwargs):
        """
        Open a file and return a stream to its content.

        seealso:: :func:`io.open`
        """
        return io.open(str(self), *args, **kwargs)

    @cached_property
    def lock(self) -> SoftFileLock:
        """
        Get a file lock holder for this file.
        """
        lock_file = self._contained.with_suffix(self.suffix + ".lock")
        if not self.isfile():
            return DummyFileLock(lock_file)
        return SoftFileLock(lock_file)

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
    def _op_context(self, name: str, timeout: float, lock: bool,
                    operation:
                    Callable[[Union[os.PathLike, path.Path], Union[os.PathLike, path.Path]], Union[str, path.Path]]):
        """
        Acquire a file mutation context that is bound to a file.
        
        :param name: the human readable name of the operation
        :param timeout: the timeout in seconds how long the lock file should be acquired
        :param lock: if the source file should be locked as long as this context is open
        :param operation: the callable operation that gets the source and target file passed as argument
        """
        if not self._contained.exists():
            raise PathException(f"{name.capitalize()} {self._contained} failed because the file does not exist.")

        try:
            if lock:
                try:
                    self.lock.acquire(timeout)
                except filelock.Timeout as t:
                    raise PathException(
                        f"{name.capitalize()} {self._contained} failed because the file could not be locked.") from t

            self.__mutable = mutapath.MutaPath(self)
            yield self.__mutable

            current_file = self._contained
            target_file = getattr(self.__mutable, "_contained")

            try:
                current_file = path.Path(operation(current_file, target_file))

            except FileExistsError as e:
                raise PathException(
                    f"{name.capitalize()} to {current_file.normpath()} failed because the file already exists. "
                    f"Falling back to original value {self._contained}.") from e

            if not current_file.exists():
                raise PathException(
                    f"{name.capitalize()} to {current_file.normpath()} failed because it can not be found. "
                    f"Falling back to original value {self._contained}.")

            self._contained = current_file

        finally:
            if self.lock.is_locked:
                self.lock.release()

    def renaming(self, lock=True, timeout=1, method: Callable[[str, str], None] = os.rename):
        """
        Create a renaming context for this immutable path.
        The external value is only changed if the renaming succeeds.

        :param timeout: the timeout in seconds how long the lock file should be acquired
        :param lock: if the source file should be locked as long as this context is open
        :param method: an alternative method that renames the path (e.g., os.renames)

        :Example:
        >>> with Path('/home/doe/folder/a.txt').renaming() as mut:
        ...     mut.stem = "b"
        Path('/home/doe/folder/b.txt')

        """

        def checked_rename(cls: path.Path, target: path.Path):
            target_lock_file = target.with_suffix(target.ext + ".lock")
            target_lock = SoftFileLock(target_lock_file)
            if lock and cls.isfile():
                try:
                    target_lock.acquire(timeout)
                except filelock.Timeout as t:
                    raise PathException(
                        f"Renaming {self._contained} failed because the target {target} could not be locked.") from t
            try:
                if target.exists():
                    raise FileExistsError(f"{target.name} already exists.")
                method(cls, target)
            finally:
                target_lock.release()
                with contextlib.suppress(PermissionError):
                    target_lock_file.remove_p()
            return target

        return self._op_context("Renaming", lock=lock, timeout=timeout, operation=checked_rename)

    def moving(self, lock=True, timeout=1, method: Callable[[os.PathLike, os.PathLike], str] = shutil.move):
        """
        Create a moving context for this immutable path.
        The external value is only changed if the moving succeeds.

        :param timeout: the timeout in seconds how long the lock file should be acquired
        :param lock: if the source file should be locked as long as this context is open
        :param method: an alternative method that moves the path and returns the new path

        >>> with Path('/home/doe/folder/a.txt').moving() as mut:
        ...     mut.stem = "b"
        Path('/home/doe/folder/b.txt')

        """
        return self._op_context("Moving", operation=method, lock=lock, timeout=timeout)

    def copying(self, lock=True, timeout=1, method: Callable[[Path, Path], Path] = shutil.copy):
        """
        Create a copying context for this immutable path.
        The external value is only changed if the copying succeeds.

        :param timeout: the timeout in seconds how long the lock file should be acquired
        :param lock: if the source file should be locked as long as this context is open
        :param method: an alternative method that copies the path and returns the new path (e.g., shutil.copy2)

        >>> with Path('/home/doe/folder/a.txt').copying() as mut:
        ...     mut.stem = "b"
        Path('/home/doe/folder/b.txt')

        """
        return self._op_context("Copying", operation=method, lock=lock, timeout=timeout)
