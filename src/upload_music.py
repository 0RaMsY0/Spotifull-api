from deta import Deta
import json
from utils.read_secret import deta_secret

deta = Deta(deta_secret()["spotifull-key"])

def upload_music(music_path: str, session_id: str):
    """
        Upload music to a deta storage
        server
    """
    MUSIC_DRIVE = deta.Drive("music")
    MUSIC_DRIVE.put(f"{music_path.replace(f'data/', '')}", open(f"{music_path}", "r"))
    