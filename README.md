# mutapath

[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/matfax/mutapath/build/master?style=for-the-badge)](https://github.com/matfax/mutapath/actions)
[![Codecov](https://img.shields.io/codecov/c/github/matfax/mutapath?style=for-the-badge)](https://codecov.io/gh/matfax/mutapath)
[![Documentation Status](https://readthedocs.org/projects/mutapath/badge/?version=latest&style=for-the-badge)](https://mutapath.readthedocs.io/en/latest/?badge=latest)
[![Dependabot Status](https://img.shields.io/badge/dependabot-enabled-blue?style=for-the-badge&logo=dependabot&color=0366d6)](https://github.com/matfax/mutapath/network/updates)
[![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/mutapath?style=for-the-badge)](https://libraries.io/pypi/mutapath)
[![CodeFactor](https://www.codefactor.io/repository/github/matfax/mutapath/badge?style=for-the-badge)](https://www.codefactor.io/repository/github/matfax/mutapath)
[![security: bandit](https://img.shields.io/badge/security-bandit-purple.svg?style=for-the-badge)](https://github.com/PyCQA/bandit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mutapath?style=for-the-badge)](https://pypi.org/project/mutapath/)
[![PyPI](https://img.shields.io/pypi/v/mutapath?color=%2339A7A6&style=for-the-badge)](https://pypi.org/project/mutapath/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/mutapath?color=ff69b4&style=for-the-badge)](https://pypistats.org/packages/mutapath)
[![GitHub License](https://img.shields.io/github/license/matfax/mutapath.svg?style=for-the-badge)](https://github.com/matfax/mutapath/blob/master/LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/matfax/mutapath?color=9cf&style=for-the-badge)](https://github.com/matfax/mutapath/commits/master)


This library is for you if you are also annoyed that there is no mutable pathlib wrapper for use cases in which paths are often changed.
mutapath solves this by wrapping both, the Python 3 pathlib library, and the alternate  [path library](https://pypi.org/project/path/), and providing a mutable context manager for them.

## MutaPath Class

The MutaPath Class allows direct mutation of its attributes at any time, just as any mutable object.
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

## Locks

Soft Locks can easily be accessed via the lazy lock property.
Moreover, the mutable context managers in `Path` (i.e., `renaming`, `moving`, `copying`) allow implicit locking.
The lock object is cached as long as the file is not mutated. 
Once the lock is mutated, it is released and regenerated, respecting the new file name.

```python
>>> my_path = Path('/home/doe/folder/sub')
>>> with my_path.lock:
...     my_path.write_text("I can write")
```

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
