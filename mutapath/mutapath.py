from dataclasses import dataclass

from mutapath import Path


@dataclass
class MutaPath(Path):
    """Mutable Path"""
    _contained: Path

    def __post_init__(self):
        if isinstance(self._contained, str):
            self._contained = Path(self._contained)

    def __getattr__(self, item):
        return getattr(self._contained, item)

    def __repr__(self):
        return repr(self._contained)

    @property
    def suffix(self) -> str:
        """Get file suffix"""
        return self._contained.ext

    @suffix.setter
    def suffix(self, value):
        """Set file suffix"""
        self._contained = self._contained.with_suffix(value)

    @property
    def name(self) -> str:
        """Get file name"""
        return self._contained.name

    @name.setter
    def name(self, value):
        """Set file name"""
        self._contained = self._contained.with_name(value)

    @property
    def base(self) -> str:
        """
        Get path base (i.e., the parent of the file)

        seealso:: :func:`pathlib.Path.parent`
        """
        return self._contained.parent

    @base.setter
    def base(self, value):
        """
        Set a new file base

        seealso:: :func:`immutapath.Path.with_base`
        """
        self._contained = self._contained.with_base(value)

    def rename(self, new):
        """Rename and mutate this path to the given new path."""
        self._contained = self._contained.rename(new)
        return self._contained

    def renames(self, new):
        """Renames and mutate this path to the given new path."""
        self._contained = self._contained.renames(new)
        return self._contained

    def copy(self, new):
        """Copy and mutate this path to the given new path."""
        self._contained = self._contained.copy(new)
        return self._contained

    def copy2(self, new):
        """Copy and mutate this path to the given new path."""
        self._contained = self._contained.copy2(new)
        return self._contained

    def copyfile(self, new):
        """Copy and mutate this file to the given new file path."""
        self._contained = self._contained.copyfile(new)
        return self._contained

    def copymode(self, other):
        """Copy and mutate this file mode to the given other file."""
        self._contained = self._contained.copymode(other)
        return self._contained

    def copystat(self, other):
        """Copy and mutate this file stat to the given other file."""
        self._contained = self._contained.copystat(other)
        return self._contained

    def copytree(self, other, symlinks=False, ignore=None, ignore_dangling_symlinks=False, **kwargs):
        """Copy and mutate this path tree to the given other path."""
        self._contained = self._contained.copytree(other, symlinks=symlinks, ignore=ignore,
                                                   ignore_dangling_symlinks=ignore_dangling_symlinks)
        return self._contained

    def move(self, new, **kwargs):
        """Move and mutate this path to the given new path."""
        self._contained = self._contained.move(new)
        return self._contained

    def merge_tree(self, other, symlinks=False, update=False, **kwargs):
        """Move, merge and mutate this path to the given other path."""
        self._contained.merge_tree(other, symlinks=symlinks, update=update)
        self._contained = other
        return self._contained
