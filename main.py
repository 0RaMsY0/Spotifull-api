import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from src.music_download_url import fetch_playlist_music_url
from utils.random_id import random_id

app = FastAPI()

@app.get("/")
def route():
    return RedirectResponse("/api/v1") 

@app.get("/api/v1", status_code=200)
def home_route():
    return {
        "status code": 200,
    }

@app.get("/api/v1/get_playlist", status_code=200)
def fetch_playlist_info(playlist_url: str):
    playlist_data = fetch_playlist_music_url(playlist_url, random_id())

    return {
        "status code": 200,
        "data": playlist_data
    }

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=1080, reload=True)