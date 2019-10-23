# mutapath

[![CircleCI](https://circleci.com/gh/matfax/mutapath/tree/master.svg?style=shield)](https://circleci.com/gh/matfax/mutapath/tree/master)
[![codecov](https://codecov.io/gh/matfax/mutapath/branch/master/graph/badge.svg)](https://codecov.io/gh/matfax/mutapath)
[![Renovate Status](https://badges.renovateapi.com/github/matfax/mutapath)](https://renovatebot.com/)
[![CodeFactor](https://www.codefactor.io/repository/github/matfax/mutapath/badge)](https://www.codefactor.io/repository/github/matfax/mutapath)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mutapath)](https://pypi.org/project/mutapath/)
[![PyPI](https://img.shields.io/pypi/v/mutapath?color=%2339A7A6)](https://pypi.org/project/mutapath/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/mutapath?color=%231447F9)](https://pypistats.org/packages/mutapath)
[![Documentation Status](https://readthedocs.org/projects/mutapath/badge/?version=latest)](https://mutapath.readthedocs.io/en/latest/?badge=latest)
[![GitHub License](https://img.shields.io/github/license/matfax/mutapath.svg)](https://github.com/matfax/mutapath/blob/master/LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/matfax/mutapath?color=%232954A5)](https://github.com/matfax/mutapath/commits/master)


This library is for you if you are also annoyed that there is no mutable pathlib wrapper for use cases where paths are often changed.
mutapath solves this by wrapping the extended pathlib library [path.py](https://pypi.org/project/path.py/) and updating the encapsulated object every time the path might be changed.

mutapath also adds the possibility to delimit file and path modifications to a safe fallback context.

## MutaPath Class

The MutaPath Class allows direct manipulation of its attributes at any time, just as any mutable object.
Once a file operation is called that is intended to modify its path, the underlying path is also mutated.

```python
>>> from mutapath import MutaPath
```
```python
>>> folder = MutaPath("/home/joe/doe/folder/sub")
>>> folder
Path('/home/joe/doe/folder/sub')
```
```python
>>> folder.name = "top"
>>> folder
Path('/home/joe/doe/folder/top')
```
```python
>>> next = MutaPath("/home/joe/doe/folder/next")
>>> next
Path('/home/joe/doe/folder/next')
```
```python
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
```
```python
>>> folder = Path("/home/joe/doe/folder/sub")
>>> folder
Path('/home/joe/doe/folder/sub')
```
```python
>>> folder.name = "top"
AttributeError: mutapath.Path is an immutable class, unless mutate() context is used.
>>> folder
Path('/home/joe/doe/folder/sub')
```
```python
>>> with folder.mutate() as m:
...     m.name = "top"
>>> folder
Path('/home/joe/doe/folder/top')
```
```python
>>> next = Path("/home/joe/doe/folder/next")
>>> next.copy(folder)
>>> next
Path('/home/joe/doe/folder/next')
>>> folder.exists()
True
>>> folder.remove()
```
```python
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


For more in-depth examples, check the tests folder.

## Hashing

mutapath paths are hashable by caching the generated hash the first time it is accessed.
However, it also adds a warning so that unintended hash usage is avoided.
Once mutated after that, the generated hashes don't provide collision detection in binary trees anymore.
Don't use them in sets or as keys in dicts.
Use the explicit string representation instead, to make the hashing input transparent.

```python
>>> p = Path("/home")
>>> hash(p)
1083235232
>>> hash(Path("/home")) == hash(p)
True
>>> with p.mutate() as m:
...     m.name = "home4"
>>> hash(p) # same hash
1083235232
>>> hash(Path("/home")) == hash(p) # they are not equal anymore
True
```
