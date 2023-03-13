import os
import time
import spotipy
from pytube import Search, YouTube

from models.music_model import Music
from utils.read_secret import *
from utils.random_id import random_id

def search_music(music_name: str):
    """
        Search for the music name 
        in youtube and returns it 
        url.
    """
    search = Search(music_name)
    results = search.results

    return results

def fetch_playlist_music_url(playlist_url: str, session_id: str, spotify_session: spotipy.Spotify, is_download: bool):
    """
        Returns a dict contains info about tracks
        in a playlist.
    """
    if "?si" in playlist_url:
        playlist_url = playlist_url.split("?si")[0]
    
    playlist = spotify_session.playlist(playlist_url)
    playlist_tracks = playlist["tracks"]

    MUSICS_INFO = []
    for track in playlist_tracks["items"]:
        # Creating Music object for tracks and adding basic information to them 

        _Music = Music()
        _Music.name = track["track"]["name"]
        _Music.publish_date = track["added_at"]
        _Music.spotify_url = track['track']['external_urls']['spotify']
        _Music.artist_name = track["track"]["album"]["name"]
        _Music.cover_image = track["track"]["album"]["images"][0]["url"]
        _Music.preview_url = track["track"]["preview_url"]
        _Music.youtube_url = f"https://youtu.be/{search_music(f'{_Music.artist_name} - {_Music.name} (Official Audio)')[0].video_id}"
        if is_download:
            _Music.download_url = download_music(_Music.youtube_url, session_id)
        pass

        MUSICS_INFO.append(_Music.to_json())

    return MUSICS_INFO

def download_music(youtube_url: Music, session_id: str) -> str:
    """
        Download wanted music list with given urls
    """
    max_retries = 7
    delay = 3
    local_music_path = None

    youtube = YouTube(youtube_url)
    music_id = random_id(20)

    if "data" not in os.listdir("."):
        os.mkdir("data")
    
    for _ in range(max_retries):
        try:
            youtube.streams.get_audio_only().download(output_path=f"data/{session_id}", filename=f"{music_id}.mp3")
            local_music_path = f"/api/v1/get_music?music_name={music_id}&session_id={session_id}"
            break
        except Exception:
            time.sleep(delay)

    return local_music_path
