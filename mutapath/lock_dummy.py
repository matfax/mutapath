from filelock import BaseFileLock


class DummyFileLock(BaseFileLock):

    def release(self, force=False):
        pass

    def acquire(self, timeout=None, poll_intervall=0.05):
        pass

    def _acquire(self):
        pass

    def _release(self):
        pass
