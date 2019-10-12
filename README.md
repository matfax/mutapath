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


```python

>>> from mutapath import MutaPath

>>> folder = MutaPath("/home/joe/doe/folder/sub")
>>> folder
Path('/home/joe/doe/folder/sub')

>>> folder.name = top
>>> folder
Path('/home/joe/doe/folder/top')

>>> next = MutaPath("/home/joe/doe/folder/next")
>>> next
Path('/home/joe/doe/folder/next')

>>> next.rename(folder)
>>> next
Path('/home/joe/doe/folder/top')

```
