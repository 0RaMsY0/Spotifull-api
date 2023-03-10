
class Music(object):
    """
        Music model helps in keeping musics
        info clean.
    """
    def __init__(self) -> None:
        self.name = ""
        self.spotify_url = ""
        self.publish_date = ""
        self.cover_image = ""
        self.artist_name = ""
        self.preview_url = ""
        self.youtube_url = ""
        self.download_url = None

    def to_json(self) -> dict:
        """
            Convert object's vars into 
            Json format.
        """
        return {
            "name": self.name,
            "spotify_url": self.spotify_url,
            "publish_date": self.publish_date,
            "artist_name": self.artist_name,
            "cover_image": self.cover_image,
            "preview_url": self.preview_url,
            "youtube_url": self.youtube_url,
            "download_url": self.download_url
        }
