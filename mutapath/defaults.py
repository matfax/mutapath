from dataclasses import dataclass

import singletons


@dataclass
class PathDefaults(metaclass=singletons.ThreadSingleton):
    """
    This dataclass contains all defaults that are used for paths if no arguments are given.
    """

    posix: bool = False
    string_repr: bool = False

    def reset(self):
        self.posix = False
        self.string_repr = False
