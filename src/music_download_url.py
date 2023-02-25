import os
import spotipy
import subprocess
from spotipy import SpotifyClientCredentials
from pytube import Search, YouTube
from models.music_model import Music
from utils.string_strip import string_strip
from utils.user_agent import ran_user_agent
from utils.random_id import random_id
from utils.read_secret import *

def search_music(music_name: str):
    """
        Search for the music name 
        in youtube and returns it 
        url.
    """
    search = Search(music_name)
    results = search.results

    return results


def fetch_playlist_music_url(playlist_url: str, session_id: str):
    """
        Returns a dict contains info about tracks
        in a playlist.
    """
    if "?si" in playlist_url:
        playlist_url = playlist_url.split("?si")[0]

    cache_handler = spotipy.CacheFileHandler(cache_path="conf/spotify-access-token")
    
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=spotify_secret()["client-id"],
        client_secret=spotify_secret()["client-secret"],
        cache_handler=cache_handler
        ),
    )
    
    playlist = spotify.playlist(playlist_url)
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
        _Music.download_url = f"https://youtu.be/{search_music(f'{_Music.artist_name} - {_Music.name} (Official Audio)')[0].video_id}"

        MUSICS_INFO.append(_Music.to_json())

    return MUSICS_INFO
