# mutapath

[![CircleCI](https://circleci.com/gh/matfax/mutapath/tree/master.svg?style=shield)](https://circleci.com/gh/matfax/mutapath/tree/master)
[![codecov](https://codecov.io/gh/matfax/mutapath/branch/master/graph/badge.svg)](https://codecov.io/gh/matfax/mutapath)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=matfax/mutapath)](https://dependabot.com)
[![CodeFactor](https://www.codefactor.io/repository/github/matfax/mutapath/badge)](https://www.codefactor.io/repository/github/matfax/mutapath)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mutapath)](https://pypi.org/project/mutapath/)
[![PyPI](https://img.shields.io/pypi/v/mutapath)](https://pypi.org/project/mutapath/)
[![GitHub License](https://img.shields.io/github/license/matfax/mutapath.svg)](https://github.com/matfax/mutapath/blob/master/LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/matfax/mutapath.svg)](https://github.com/matfax/mutapath/commits/master)

This library is for you if you are also annoyed that there is no mutable pathlib wrapper for use cases where paths are often changed.
mutapath solves this by wrapping the extended pathlib library path.py and updating the encapsulated object every time the path might be changed.

mutapath also adds the possibility to delimit file and path modifications to a safe fallback context.

## MutaPath Class

The MutaPath Class allows direct manipulation of its attributes at any time, just as any mutable object.
Once a file operation is called that is intended to modify its path, the underlying path is also mutated.

```python

>>> from mutapath import MutaPath

>>> folder = MutaPath("/home/joe/doe/folder/sub")
>>> folder
Path('/home/joe/doe/folder/sub')

>>> folder.name = "top"
>>> folder
Path('/home/joe/doe/folder/top')

>>> next = MutaPath("/home/joe/doe/folder/next")
>>> next
Path('/home/joe/doe/folder/next')

>>> next.rename(folder)
>>> next
Path('/home/joe/doe/folder/top')
>>> next.exists()
True
>>> Path('/home/joe/doe/folder/sub').exists()
False

```

## Path Class

This class is immutable by default, just as the `pathlib.Path`. However, it allows to open a editing context via `mutate()`.
Moreover, there are additional contexts for file operations. They update the file and its path while closing the context.
If the file operations don't succeed, they throw an exception and fall back to the original path value.

```python

>>> from mutapath import Path

>>> folder = Path("/home/joe/doe/folder/sub")
>>> folder
Path('/home/joe/doe/folder/sub')

>>> folder.name = "top"
AttributeError: mutapath.Path is an immutable class, unless mutate() context is used.
>>> folder
Path('/home/joe/doe/folder/sub')

>>> with folder.mutate() as m:
...     m.name = "top"
>>> folder
Path('/home/joe/doe/folder/top')

>>> next = Path("/home/joe/doe/folder/next")
>>> next.copy(folder)
>>> next
Path('/home/joe/doe/folder/next')
>>> folder.exists()
True
>>> folder.remove()

>>> with next.renaming() as m:
...     m.stem = folder.stem
...     m.suffix = ".txt"
>>> next
Path("/home/joe/doe/folder/sub.txt")
>>> next.exists()
True
>>> next.with_name("next").exists()
False

```
