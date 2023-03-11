import os
import threading

from utils.date import hour
from .session_expire_thread import track_sessions

class ThreadsManager (object):
    """
        Manage all the API threads
    """
    global THREADS, RUNNING_THREADS, EVENT
    
    THREADS = [
        track_sessions,
    ]
    RUNNING_THREADS = []
    EVENT = threading.Event()

    def __init__(self) -> None:
        pass

    def init_threads() -> None:
        """
            Starts all the threads when initialasing
            the programe
        """

        for thread in THREADS:
            _thread = threading.Thread(target=thread, args=(EVENT,))
            RUNNING_THREADS.append(_thread)
            _thread.start()

    def stop_threads() -> None:
        """
            Stoping all the threads
        """
        EVENT.set()
