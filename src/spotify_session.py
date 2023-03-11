import spotipy
from spotipy import SpotifyClientCredentials

from utils.read_secret import spotify_secret

def spotify_session() -> spotipy.Spotify:
    """
        Start a Spotipy session to use instead of
        calling the api every time a user makes
        a requests
    """
    cache_handler = spotipy.CacheFileHandler(cache_path="conf/spotify-access-token")
    
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=spotify_secret()["client-id"],
        client_secret=spotify_secret()["client-secret"],
        cache_handler=cache_handler
        ),
    )

    return spotify

