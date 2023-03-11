import os
import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse, StreamingResponse

from src.music_download_url import fetch_playlist_music_url
from src.spotify_session import spotify_session
from src.api_threads.threads import ThreadsManager
from src.database import Database
from utils.random_id import random_id
from utils.read_api_config import read_api_config

app = FastAPI()

# Consts
SPOTIFY_SESSION = spotify_session()
DATABASE = Database()
THREADS_MANAGER = ThreadsManager()

@app.get("/")
def route():
    print(DATABASE.get_sessions())
    return RedirectResponse("/api/v1")

@app.get("/api/v1", status_code=200)
def home_route():
    return {
        "status code": 200,
    }

@app.get("/api/v1/get_playlist", status_code=200)
def playlist_info(playlist_url: str):
    global SPOTIFY_SESSION

    api_config = read_api_config()
    session_id = random_id(); DATABASE.add_session(session_id)
    playlist_data = fetch_playlist_music_url(playlist_url, session_id, SPOTIFY_SESSION, api_config["enable_local_download"])

    return {
        "status code": 200,
        "session_id": session_id,
        "data": playlist_data
    }

# read/download music
@app.get("/api/v1/get_music")
def get_music(music_name: str, session_id: str):
    if session_id not in os.listdir("data"):
        return {
            "status_code": 404,
            "error message": "session_id not found",
        }
    if music_name in os.listdir(f"data/{session_id}"):
        def iter_file():
            with open(f"data/{session_id}/{music_name}", "rb") as req_music:
                yield from req_music
        return StreamingResponse(iter_file(), media_type="audio/mp3")
    else:
        return {
            "status_code": 404,
            "error message": "music name not found",
        }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9067, reload=True)
