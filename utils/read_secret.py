import json

def spotify_secret():
    """
        Returns a dict of spotify secret
        id, secret etc...
    """
    data = None
    with open("conf/spotify-secret.json", "r") as secrets:
        data = json.load(secrets)

    return data

def deta_secret():
    """
        Return a dict that contains
        secret of deta. like the 
        project key ...
    """
    data = None
    with open("conf/deta-secret.json", "r") as deta:
        data = json.load(deta)

    return data