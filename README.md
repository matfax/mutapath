# mutapath

[![CircleCI](https://circleci.com/gh/matfax/mutapath/tree/master.svg?style=shield)](https://circleci.com/gh/matfax/mutapath/tree/master)
[![codecov](https://codecov.io/gh/matfax/mutapath/branch/master/graph/badge.svg)](https://codecov.io/gh/matfax/mutapath)

This library is for you if you are also annoyed that there is no mutable pathlib wrapper for use cases where paths are often changed.
mutapath solves this by wrapping the extended pathlib library path.py and updating the encapsulated object every time the path might be changed.
