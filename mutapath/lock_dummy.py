from filelock import BaseFileLock


class DummyFileLock(BaseFileLock):

    def release(self, force=False):
        """Doing nothing"""

    def acquire(self, timeout=None, poll_intervall=0.05):
        """Doing nothing"""

    def _acquire(self):
        """Doing nothing"""

    def _release(self):
        """Doing nothing"""
