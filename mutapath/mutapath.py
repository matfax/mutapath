from __future__ import annotations

import pathlib
from typing import Union, Optional

import path

import mutapath
from mutapath.decorator import mutable_path_wrapper


@mutable_path_wrapper
class MutaPath(mutapath.Path):
    """Mutable Path"""

    def __init__(self, contained: Union[MutaPath, mutapath.Path, path.Path, pathlib.PurePath, str] = "", *,
                 posix: Optional[bool] = None,
                 string_repr: Optional[bool] = None):
        if isinstance(contained, MutaPath):
            contained = contained._contained
        super(MutaPath, self).__init__(contained, posix=posix, string_repr=string_repr)

    def __eq__(self, other):
        return super(MutaPath, self).__eq__(other)

    def __hash__(self):
        return super(MutaPath, self).__hash__()

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)
        if key == "_contained":
            if isinstance(value, mutapath.Path):
                value = value._contained
            self._set_contained(value)

    def merge_tree(self, other, *args, **kwargs):
        """Move, merge and mutate this path to the given other path."""
        self._contained.merge_tree(other, *args, **kwargs)
        self._contained = other
        return self
