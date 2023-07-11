# mutapath

[![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/matfax/mutapath/build.yml?branch=main&style=for-the-badge)](https://github.com/matfax/mutapath/actions)
[![Codecov](https://img.shields.io/codecov/c/github/matfax/mutapath?style=for-the-badge)](https://codecov.io/gh/matfax/mutapath)
[![Documentation Status](https://readthedocs.org/projects/mutapath/badge/?version=latest&style=for-the-badge)](https://mutapath.readthedocs.io/en/latest/?badge=latest)
[![Renovate Bot](https://img.shields.io/badge/renovate-enabled-green?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjUgNSAzNzAgMzcwIj48Y2lyY2xlIGN4PSIxODkiIGN5PSIxOTAiIHI9IjE4NCIgZmlsbD0iI2ZlMiIvPjxwYXRoIGZpbGw9IiM4YmIiIGQ9Ik0yNTEgMjU2bC0zOC0zOGExNyAxNyAwIDAxMC0yNGw1Ni01NmMyLTIgMi02IDAtN2wtMjAtMjFhNSA1IDAgMDAtNyAwbC0xMyAxMi05LTggMTMtMTNhMTcgMTcgMCAwMTI0IDBsMjEgMjFjNyA3IDcgMTcgMCAyNGwtNTYgNTdhNSA1IDAgMDAwIDdsMzggMzh6Ii8+PHBhdGggZmlsbD0iI2Q1MSIgZD0iTTMwMCAyODhsLTggOGMtNCA0LTExIDQtMTYgMGwtNDYtNDZjLTUtNS01LTEyIDAtMTZsOC04YzQtNCAxMS00IDE1IDBsNDcgNDdjNCA0IDQgMTEgMCAxNXoiLz48cGF0aCBmaWxsPSIjYjMwIiBkPSJNMjg1IDI1OGw3IDdjNCA0IDQgMTEgMCAxNWwtOCA4Yy00IDQtMTEgNC0xNiAwbC02LTdjNCA1IDExIDUgMTUgMGw4LTdjNC01IDQtMTIgMC0xNnoiLz48cGF0aCBmaWxsPSIjYTMwIiBkPSJNMjkxIDI2NGw4IDhjNCA0IDQgMTEgMCAxNmwtOCA3Yy00IDUtMTEgNS0xNSAwbC05LThjNSA1IDEyIDUgMTYgMGw4LThjNC00IDQtMTEgMC0xNXoiLz48cGF0aCBmaWxsPSIjZTYyIiBkPSJNMjYwIDIzM2wtNC00Yy02LTYtMTctNi0yMyAwLTcgNy03IDE3IDAgMjRsNCA0Yy00LTUtNC0xMSAwLTE2bDgtOGM0LTQgMTEtNCAxNSAweiIvPjxwYXRoIGZpbGw9IiNiNDAiIGQ9Ik0yODQgMzA0Yy00IDAtOC0xLTExLTRsLTQ3LTQ3Yy02LTYtNi0xNiAwLTIybDgtOGM2LTYgMTYtNiAyMiAwbDQ3IDQ2YzYgNyA2IDE3IDAgMjNsLTggOGMtMyAzLTcgNC0xMSA0em0tMzktNzZjLTEgMC0zIDAtNCAybC04IDdjLTIgMy0yIDcgMCA5bDQ3IDQ3YTYgNiAwIDAwOSAwbDctOGMzLTIgMy02IDAtOWwtNDYtNDZjLTItMi0zLTItNS0yeiIvPjxwYXRoIGZpbGw9IiMxY2MiIGQ9Ik0xNTIgMTEzbDE4LTE4IDE4IDE4LTE4IDE4em0xLTM1bDE4LTE4IDE4IDE4LTE4IDE4em0tOTAgODlsMTgtMTggMTggMTgtMTggMTh6bTM1LTM2bDE4LTE4IDE4IDE4LTE4IDE4eiIvPjxwYXRoIGZpbGw9IiMxZGQiIGQ9Ik0xMzQgMTMxbDE4LTE4IDE4IDE4LTE4IDE4em0tMzUgMzZsMTgtMTggMTggMTgtMTggMTh6Ii8+PHBhdGggZmlsbD0iIzJiYiIgZD0iTTExNiAxNDlsMTgtMTggMTggMTgtMTggMTh6bTU0LTU0bDE4LTE4IDE4IDE4LTE4IDE4em0tODkgOTBsMTgtMTggMTggMTgtMTggMTh6bTEzOS04NWwyMyAyM2M0IDQgNCAxMSAwIDE2TDE0MiAyNDBjLTQgNC0xMSA0LTE1IDBsLTI0LTI0Yy00LTQtNC0xMSAwLTE1bDEwMS0xMDFjNS01IDEyLTUgMTYgMHoiLz48cGF0aCBmaWxsPSIjM2VlIiBkPSJNMTM0IDk1bDE4LTE4IDE4IDE4LTE4IDE4em0tNTQgMThsMTgtMTcgMTggMTctMTggMTh6bTU1LTUzbDE4LTE4IDE4IDE4LTE4IDE4em05MyA0OGwtOC04Yy00LTUtMTEtNS0xNiAwTDEwMyAyMDFjLTQgNC00IDExIDAgMTVsOCA4Yy00LTQtNC0xMSAwLTE1bDEwMS0xMDFjNS00IDEyLTQgMTYgMHoiLz48cGF0aCBmaWxsPSIjOWVlIiBkPSJNMjcgMTMxbDE4LTE4IDE4IDE4LTE4IDE4em01NC01M2wxOC0xOCAxOCAxOC0xOCAxOHoiLz48cGF0aCBmaWxsPSIjMGFhIiBkPSJNMjMwIDExMGwxMyAxM2M0IDQgNCAxMSAwIDE2TDE0MiAyNDBjLTQgNC0xMSA0LTE1IDBsLTEzLTEzYzQgNCAxMSA0IDE1IDBsMTAxLTEwMWM1LTUgNS0xMSAwLTE2eiIvPjxwYXRoIGZpbGw9IiMxYWIiIGQ9Ik0xMzQgMjQ4Yy00IDAtOC0yLTExLTVsLTIzLTIzYTE2IDE2IDAgMDEwLTIzTDIwMSA5NmExNiAxNiAwIDAxMjIgMGwyNCAyNGM2IDYgNiAxNiAwIDIyTDE0NiAyNDNjLTMgMy03IDUtMTIgNXptNzgtMTQ3bC00IDItMTAxIDEwMWE2IDYgMCAwMDAgOWwyMyAyM2E2IDYgMCAwMDkgMGwxMDEtMTAxYTYgNiAwIDAwMC05bC0yNC0yMy00LTJ6Ii8+PC9zdmc+)](https://github.com/matfax/mutapath/issues/270)
[![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/mutapath?style=for-the-badge)](https://libraries.io/pypi/mutapath)
[![CodeFactor](https://www.codefactor.io/repository/github/matfax/mutapath/badge?style=for-the-badge)](https://www.codefactor.io/repository/github/matfax/mutapath)
[![security: bandit](https://img.shields.io/badge/security-bandit-purple.svg?style=for-the-badge)](https://github.com/PyCQA/bandit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mutapath?style=for-the-badge)](https://pypi.org/project/mutapath/)
[![PyPI](https://img.shields.io/pypi/v/mutapath?color=%2339A7A6&style=for-the-badge)](https://pypi.org/project/mutapath/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/mutapath?color=ff69b4&style=for-the-badge)](https://pypistats.org/packages/mutapath)
[![GitHub Release Date](https://img.shields.io/github/release-date/matfax/mutapath?color=%23986293&style=for-the-badge)](https://github.com/matfax/mutapath/releases)
[![GitHub last commit](https://img.shields.io/github/last-commit/matfax/mutapath?color=9cf&style=for-the-badge)](https://github.com/matfax/mutapath/commits/main)
[![GitHub License](https://img.shields.io/github/license/matfax/mutapath.svg?style=for-the-badge)](https://github.com/matfax/mutapath/blob/main/LICENSE)

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
