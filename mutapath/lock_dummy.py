from filelock import BaseFileLock


class DummyFileLock(BaseFileLock):

    def release(self, force=False):
        """Doing nothing"""
        pass

    def acquire(self, timeout=None, poll_intervall=0.05):
        """Doing nothing"""
        pass

    def _acquire(self):
        """Doing nothing"""
        pass

    def _release(self):
        """Doing nothing"""
        pass
