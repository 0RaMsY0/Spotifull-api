import os
import sys
import uvicorn
import logging
from loguru import logger
from fastapi import FastAPI
from contextlib import asynccontextmanager
from starlette.responses import RedirectResponse, StreamingResponse

from utils.random_id import random_id
from utils.iterate_file import iter_file
from utils.read_api_config import read_api_config
from src.music_download_url import fetch_playlist_music_url
from src.spotify_session import spotify_session
from src.api_threads.threads import ThreadsManager
from src.api_threads.session_expire_thread import TrackSessions
from src.database import Database
from src.logs import InterceptHandler, StandaloneApplication, LOG_LEVEL, JSON_LOGS, WORKERS, StubbedGunicornLogger

# Consts
SPOTIFY_SESSION = spotify_session()
DATABASE = Database()
THREADS_MANAGER = ThreadsManager()

# Check for `logs/` directory
if "logs" not in os.listdir("."):
    os.mkdir("logs")
pass

app = FastAPI()

@app.on_event("startup")
async def startup_event() -> None:
    """
        Starting all the needed 
        threads
    """
    THREADS_MANAGER.init_threads()

@app.on_event("shutdown")
def shutown_event() -> None:
    """
        Stop all the alive threads
    """
    THREADS_MANAGER.stop_threads()

@app.get("/")
def route():
    return RedirectResponse("/api/v1")

@app.get("/api/v1", status_code=200)
def home_route():
    """
        Home Route
    """
    return {
        "status code": 200,
    }

@app.get("/api/v1/get_playlist", status_code=200)
def playlist_info(playlist_url: str):
    """
        Returns the requested playlist data
        in a json format
        [NOTE]: In case ```enable_local_download``` was 
            set to true it will download the music from
            that playlist and serve it.
    """
    global SPOTIFY_SESSION

    api_config = read_api_config()
    session_id = random_id(10); DATABASE.add_session(session_id)
    playlist_data = fetch_playlist_music_url(playlist_url, session_id, SPOTIFY_SESSION, api_config["enable_local_download"])

    return {
        "status code": 200,
        "session_id": session_id,
        "data": playlist_data
    }

# read/download music
@app.get("/api/v1/get_music")
def get_music(music_id: str, session_id: str):
    """
        Returns the selected music based
        on it's id
    """
    if session_id not in os.listdir("data"):
        return {
            "status_code": 404,
            "error message": "session_id not found",
        }
    if music_id in [i.replace(".mp3", "") for i in os.listdir(f"data/{session_id}")]:
        return StreamingResponse(iter_file(f"data/{session_id}/{music_id}.mp3"), media_type="audio/mp3")
    else:
        return {
            "status_code": 404,
            "error message": "music name not found",
        }

@app.get("/api/v1/server.log")
def server_logs():
    """
        Returns the `logs/server.log` file
    """
    return StreamingResponse(iter_file("logs/server.log"), media_type="text/plain")

if __name__ == "__main__":
    intercept_handler = InterceptHandler()
    # logging.basicConfig(handlers=[intercept_handler], level=LOG_LEVEL)
    # logging.root.handlers = [intercept_handler]
    logging.root.setLevel(LOG_LEVEL)

    seen = set()
    for name in [
        *logging.root.manager.loggerDict.keys(),
        "gunicorn",
        "gunicorn.access",
        "gunicorn.error",
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
    ]:
        if name not in seen:
            seen.add(name.split(".")[0])
            logging.getLogger(name).handlers = [intercept_handler]

    logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS}])
    logger.add("logs/server.log", rotation="100 MB")

    options = {
        "bind": "0.0.0.0:9898",
        "workers": WORKERS,
        "accesslog": "-",
        "errorlog": "-",
        "worker_class": "uvicorn.workers.UvicornWorker",
        "logger_class": StubbedGunicornLogger
    }

    StandaloneApplication(app, options).run()
