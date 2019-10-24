from __future__ import annotations

import contextlib
import io
import os
import pathlib
import shutil
import warnings
from contextlib import contextmanager
from typing import Union, Iterable, Callable, Optional

import filelock
import path
from cached_property import cached_property
from filelock import SoftFileLock

import mutapath
from mutapath.decorator import path_wrapper
from mutapath.defaults import PathDefaults
from mutapath.exceptions import PathException
from mutapath.lock_dummy import DummyFileLock

try:
    from mashumaro.types import SerializableType
except ImportError:
    SerializableType = object
except NotImplementedError:
    SerializableType = object


@path_wrapper
class Path(SerializableType):
    """Immutable Path"""
    _contained: Union[path.Path, pathlib.PurePath, str] = path.Path("")
    __always_posix_format: bool
    __string_repr: bool
    __mutable: object

    def __init__(self, contained: Union[Path, path.Path, pathlib.PurePath, str] = "", *,
                 posix: Optional[bool] = None,
                 string_repr: Optional[bool] = None):
        if posix is None:
            posix = PathDefaults().posix
        self.__always_posix_format = posix

        if string_repr is None:
            string_repr = PathDefaults().string_repr
        self.__string_repr = string_repr

        self._set_contained(contained, posix)
        super().__init__()

    def _set_contained(self, contained: Union[Path, path.Path, pathlib.PurePath, str], posix: Optional[bool] = None):
        if contained:
            if isinstance(contained, Path):
                contained = contained._contained
            elif isinstance(contained, pathlib.PurePath):
                contained = str(contained)

            normalized = path.Path.module.normpath(contained)
            if (posix is None and self.__always_posix_format) or posix:
                normalized = Path.posix_string(normalized)
            else:
                normalized = Path._shorten_duplicates(normalized)

            contained = path.Path(normalized)

            super(Path, self).__setattr__("_contained", contained)

    def __dir__(self) -> Iterable[str]:
        return sorted(super(Path, self).__dir__()) + dir(path.Path)

    def __getitem__(self, item):
        return self._contained.__getitem__(item)

    def __getattr__(self, item):
        return getattr(self._contained, item)

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
            self._set_contained(value)
        elif key in ["_Path__mutable", "_Path__always_posix_format", "_Path__string_repr"]:
            super(Path, self).__setattr__(key, value)
        else:
            raise AttributeError(f"attribute {key} can not be set because mutapath.Path is an immutable class.")

    def __repr__(self):
        if self.__string_repr:
            return self.__str__()
        return Path._shorten_duplicates(repr(self._contained))

    def __str__(self):
        if self.posix_enabled:
            return self.posix_string()
        return self._shorten_duplicates()

    def __eq__(self, other):
        if isinstance(other, pathlib.PurePath):
            other = str(other)
        elif isinstance(other, Path):
            other = other._contained

        if isinstance(other, str):
            if self._contained == other:
                return True
            other = path.Path(other)
        if isinstance(other, path.Path):
            if self._contained == other:
                return True
            other = Path(other, posix=self.__always_posix_format)

        if not isinstance(other, Path):
            return NotImplemented

        return str(self) == str(other)

    def __hash__(self):
        warnings.warn(f"It is not advised to hash mutable path objects or to use them in sets or dicts. "
                      f"Please use hash(str(path)) instead to make the actual hashing input transparent.",
                      category=SyntaxWarning)
        return self._hash_cache

    @cached_property
    def _hash_cache(self) -> int:
        return hash(self._contained)

    def __lt__(self, other):
        if isinstance(other, Path):
            return self.splitall() < other.splitall()
        left = self.posix_string()
        right = Path.posix_string(str(other))
        return left < right

    def __le__(self, other):
        if isinstance(other, Path):
            return self.splitall() <= other.splitall()
        left = self.posix_string()
        right = Path.posix_string(str(other))
        return left <= right

    def __gt__(self, other):
        if isinstance(other, Path):
            return self.splitall() > other.splitall()
        left = self.posix_string()
        right = Path.posix_string(str(other))
        return left > right

    def __ge__(self, other):
        if isinstance(other, Path):
            return self.splitall() >= other.splitall()
        left = self.posix_string()
        right = Path.posix_string(str(other))
        return left >= right

    def __add__(self, other) -> str:
        return str(self.clone(self._contained.__add__(Path(other)._contained)))

    def __radd__(self, other) -> str:
        return str(self.clone(self._contained.__radd__(Path(other)._contained)))

    def __div__(self, other):
        return self._contained.__div__(Path(other)._contained)

    __truediv__ = __div__

    def __rdiv__(self, other):
        return self._contained.__rdiv__(Path(other)._contained)

    __rtruediv__ = __rdiv__

    def __enter__(self):
        return self.clone(self._contained.__enter__())

    def __exit__(self, *_):
        self._contained.__exit__()

    def __fspath__(self):
        return self._contained.__fspath__()

    def __invert__(self):
        """Create a cloned :class:`~mutapath.MutaPath` from this immutable Path."""
        from mutapath import MutaPath
        return MutaPath(self._contained, posix=self.posix_enabled)

    def _serialize(self) -> str:
        return str(self._contained)

    @classmethod
    def _deserialize(cls, value: str) -> Path:
        return cls(value)

    @property
    def to_pathlib(self) -> pathlib.Path:
        """
        Return the contained path as pathlib.Path representation.
        :return: the converted path
        """
        return pathlib.Path(self._contained)

    def clone(self, contained) -> Path:
        """
        Clone this path with a new given wrapped path representation, having the same remaining attributes.
        :param contained: the new contained path element
        :return: the cloned path
        """
        return Path(contained, posix=self.__always_posix_format, string_repr=self.__string_repr)

    @path.multimethod
    def _shorten_duplicates(self, input_path: str = "") -> str:
        if isinstance(input_path, Path):
            input_path = input_path._contained
        return input_path.replace('\\\\', '\\')

    @path.multimethod
    def posix_string(self, input_path: str = "") -> str:
        """
        Get this path as string with posix-like separators (i.e., '/').

        :Example:
        >>> Path("\\home\\\\doe/folder\\sub").with_poxis_enabled()
        '/home/joe/doe/folder/sub'
        """
        if isinstance(input_path, Path):
            input_path = input_path._contained
        return input_path.replace('\\\\', '\\').replace('\\', '/')

    def with_poxis_enabled(self, enable: bool = True) -> Path:
        """
        Clone this path in posix format with posix-like separators (i.e., '/').

        :Example:
        >>> Path("\\home\\\\doe/folder\\sub").with_poxis_enabled()
        Path('/home/joe/doe/folder/sub')
        """
        return Path(self, posix=enable, string_repr=self.__string_repr)

    def with_string_repr_enabled(self, enable: bool = True) -> Path:
        """
        Clone this path in with string representation enabled.

        :Example:
        >>> Path("/home/doe/folder/sub").with_string_repr_enabled()
        '/home/joe/doe/folder/sub'
        """
        return Path(self, posix=self.__always_posix_format, string_repr=enable)

    def with_name(self, new_name) -> Path:
        """ .. seealso:: :func:`pathlib.PurePath.with_name` """
        return self.base.joinpath(str(new_name))

    def with_stem(self, new_stem) -> Path:
        """Clone this path with a new stem."""
        return self.base.joinpath(str(new_stem)).with_suffix(self.ext)

    def with_parent(self, new_parent) -> Path:
        """Clone this path with a new parent."""
        return Path(new_parent) / self.name

    def with_base(self, base, strip_length: int = 0):
        """
        Clone this path with a new base.

        The given path is used in its full length as base of this path, if strip_length is not specified.

        :Example:
        >>> Path('/home/doe/folder/sub').with_base("/home/joe")
        Path('/home/joe/folder/sub')

        If strip_length is specified, the given number of path elements are stripped from the left side,
        and the given base is prepended.

        :Example:
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
        """ .. seealso:: :func:`pathlib.Path.cwd` """
        return Path(os.getcwd())

    @property
    def cwd(self):
        """ .. seealso:: :func:`pathlib.Path.cwd` """
        return self.getcwd()

    @path.multimethod
    def joinpath(self, first, *others) -> Path:
        """ .. seealso:: :func:`pathlib.PurePath.joinpath` """
        contained_others = map(str, others)
        safe_instance = first
        if not isinstance(safe_instance, Path):
            safe_instance = Path(safe_instance)
        joined = path.Path.joinpath(safe_instance._contained, *contained_others)
        return Path(joined, posix=safe_instance.posix_enabled)

    @property
    def home(self) -> Path:
        """
        Get the home path of the current path representation.

        :return: the home path

        :Example:
        >>> Path("/home/doe/folder/sub").home
        Path("home")
        """
        split = self.splitall()
        if len(split) <= 1:
            return self.drive
        for parent in self.parents:
            if parent.name == split[1]:
                return parent.name
        return self.drive

    @property
    def string_repr_enabled(self) -> bool:
        """
        If set to True, the the representation of this path will always be returned unwrapped as the path's string.
        """
        return self.__string_repr

    @property
    def posix_enabled(self) -> bool:
        """
        If set to True, the the representation of this path will always follow the posix format, even on NT filesystems.
        """
        return self.__always_posix_format

    @posix_enabled.setter
    def posix_enabled(self, value: bool):
        self.__always_posix_format = value

    @property
    def suffix(self) -> str:
        """ .. seealso:: :attr:`pathlib.PurePath.suffix` """
        return self.ext

    @suffix.setter
    def suffix(self, value):
        self._contained = self.with_suffix(value)

    @property
    def name(self) -> Path:
        """ .. seealso:: :attr:`pathlib.PurePath.name` """
        return self.clone(self._contained.name)

    @name.setter
    def name(self, value):
        self._contained = self.with_name(value)

    @property
    def base(self) -> Path:
        """
        Get the path base (i.e., the parent of the file).

        .. seealso:: :attr:`parent`
        """
        return self.clone(self._contained.parent)

    @base.setter
    def base(self, value):
        self._contained = self.with_base(value)

    @property
    def stem(self) -> str:
        """ .. seealso:: :attr:`pathlib.PurePath.stem` """
        return self._contained.stem

    @stem.setter
    def stem(self, value):
        self._contained = self.with_stem(value)

    @property
    def parent(self) -> Path:
        """ .. seealso:: :attr:`pathlib.PurePath.parent` """
        return self.clone(self._contained.parent)

    @parent.setter
    def parent(self, value):
        self._contained = self.with_parent(value)

    @property
    def dirname(self) -> Path:
        """ .. seealso:: :func:`os.path.dirname` """
        return self.clone(self._contained.dirname())

    def open(self, *args, **kwargs):
        """ .. seealso:: :func:`pathlib.Path.open` """
        return io.open(str(self), *args, **kwargs)

    def glob(self, pattern):
        """ .. seealso:: :func:`pathlib.Path.glob` """
        paths = self.to_pathlib.glob(pattern)
        return (self.clone(g) for g in paths)

    @cached_property
    def lock(self) -> filelock.BaseFileLock:
        """
        Generate a cached file locker for this file with the additional suffix '.lock'.
        If this path refers not to an existing file or to an existing folder,
        a dummy lock is returned that does not do anything.

        Once this path is modified (cloning != modifying), the lock is released and regenerated for the new path.

        :Example:
        >>> my_path = Path('/home/doe/folder/sub')
        >>> with my_path.lock:
        ...     my_path.write_text("I can write")

        .. seealso:: :class:`~filelock.SoftFileLock`, :class:`~mutapath.lock_dummy.DummyFileLock`
        """
        lock_file = self._contained.with_suffix(self.suffix + ".lock")
        if not self.isfile():
            return DummyFileLock(lock_file)
        return SoftFileLock(lock_file)

    @contextmanager
    def mutate(self):
        """
        Create a mutable context for this immutable path.

        :Example:
        >>> with Path('/home/doe/folder/sub').mutate() as mut:
        ...     mut.name = "top"
        Path('/home/doe/folder/top')
        """
        self.__mutable = mutapath.MutaPath(self)
        yield self.__mutable
        self._contained = self.__mutable._contained

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
            target_file = self.__mutable._contained

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

        :Example:
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

        :Example:
        >>> with Path('/home/doe/folder/a.txt').copying() as mut:
        ...     mut.stem = "b"
        Path('/home/doe/folder/b.txt')
        """
        return self._op_context("Copying", operation=method, lock=lock, timeout=timeout)
