import path


class Path(path.Path):
    """Immutable Path"""

    def with_name(self, new_name):
        """
        Clone this path with a new name

        .. seealso:: :func:`pathlib.Path.with_name`
        """
        return self.parent.joinpath(new_name)

    def with_base(self, base, strip_length: int = 0):
        """
        Clone this path with a new base.

        The given path is used in its full length as base of this path, if strip_length is not specified.
        If strip_length is specified, the given number of path elements are stripped from the left side,
        and the given base is prepended.

        >>> Path('/home/doe/folder/sub').with_base("/home/joe")
        Path('/home/joe/folder/sub')

        >>> Path('/home/doe/folder/sub').with_base("/home/joe", strip_length=1)
        Path('/home/joe/doe/folder/sub')

        """
        base = self._next_class(base)
        if not strip_length:
            strip_length = len(base.splitall())
        else:
            strip_length += 1

        if len(self.splitall()) <= strip_length:
            raise ValueError("The given base has more elements than this path.")
        stripped = Path.joinpath(*self.splitall()[strip_length:])
        return base.joinpath(stripped)
