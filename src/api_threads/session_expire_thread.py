import time
import threading

from utils.date import hour, today

class TrackSessions(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self._stop_event = threading.Event()

    def stop(self) -> None:
        self._stop_event.set()

    def run(self) -> None:
        """
            Thread function to track sessions if
            the 24h has passed since the creation 
            of it, it will be deleted along with 
            the music that got downloaded during 
            it.
        """
        from main import DATABASE
        delay_time = 60
        # [NOTE]: if you decrease the delay and you 
        # have a weak hardware it may cause problems
        # specilly if the database contains a lot of
        # sessions.

        while True:
            if self._stop_event.is_set():
                break
            registered_sessions = DATABASE.get_sessions()
            current_hour = hour()
            current_day = today()
            for session in registered_sessions:
                session_id = session[0]
                session_date = session[1].split("-")
                if int(session_date[-2]) == current_day:
                    continue
                else:
                    if int(session_date[-1]) >= current_hour:
                        DATABASE.delete_session(session_id)
                    else:
                        continue

            time.sleep(delay_time)
