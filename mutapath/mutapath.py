from dataclasses import dataclass

import mutapath
from mutapath.decorator import path_mutable


@path_mutable
@dataclass(repr=False, eq=False)
class MutaPath(mutapath.Path):
    """Mutable Path"""

    def __post_init__(self):
        if isinstance(self._contained, MutaPath):
            self._contained = self._contained._contained
        super(MutaPath, self).__post_init__()

    def __eq__(self, other):
        if isinstance(other, mutapath.MutaPath):
            return self._contained == other._contained
        return super(MutaPath, self).__eq__(other)

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)
        if key == "_contained":
            self.__post_init__()

    def __repr__(self):
        return repr(self._contained)

    def __str__(self):
        return self._contained

    def merge_tree(self, other, *args, **kwargs):
        """Move, merge and mutate this path to the given other path."""
        self._contained.merge_tree(other, *args, **kwargs)
        self._contained = other
        return self
