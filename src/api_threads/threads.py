import threading

from .session_expire_thread import TrackSessions

class ThreadsManager (object):
    """
        Manage all the API threads
    """
    global THREADS, RUNNING_THREADS, EVENT
    THREADS = [
        TrackSessions(),
    ]
    RUNNING_THREADS = []

    def __init__(self) -> None:
        pass

    def init_threads(self) -> None:
        """
            Starts all the threads
        """
        for thread in THREADS:
            thread.start()

    def stop_threads(self) -> None:
        """
            Stoping all the threads
        """
        for thread in THREADS:
            thread.stop()
