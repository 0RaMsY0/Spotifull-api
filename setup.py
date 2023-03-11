import os
import sys
import json
import argparse


def setup_spotify_conf() -> None:
    """
        Setup the spotify configue
    """
    CONF_DATA = {
        "client-id": "",
        "client-secret": "",
        "redirect-url": ""
    }

    print("[  !  ] Spotify configue setup")

    if "spotify-secret.json" in os.listdir("./conf"):
        print("[  +  ] Spotify configue detected `skipping`")
        sys.exit(0)
    
    client_id = input(" ==> Enter your client ID: ")
    client_secret = input(" ==> Enter your client secret: ")
    redirect_url = input(" ==> Enter you redirect url: ")
    
    if client_id == "" or client_secret == "" or redirect_url == "":
        print("[  ?  ] Error: you need to fill in the data")
        sys.exit(1)

    CONF_DATA["client-id"] = client_id
    CONF_DATA["client-secret"] = client_secret
    CONF_DATA["redirect-url"] = redirect_url
    
    with open("conf/spotify-secret.json", "w") as save_conf:
        json.dump(CONF_DATA, save_conf)

    print("[  +  ] Spotify configue saved `conf/spotify-secret.json`")


def setup_deps() -> None:
    """
        Download the needed deps
    """
    print("[  +  ] Downloading deps...")
    os.system("pip install -r requirements.txt")


def run(args) -> None:
    """
        Init setup
    """
    SETUP_ALL = args.setup_all
    SETUP_DEPS = args.setup_deps
    SETUP_CONF = args.setup_configues

    if SETUP_ALL == False and SETUP_DEPS == False and SETUP_CONF == False:
        print("[  !  ] Error: no flags parsed [ use --help to see options]")
        sys.exit(1)
    
    if SETUP_ALL:
        setup_deps()
        setup_spotify_conf()
    elif SETUP_CONF:
        setup_spotify_conf()
    elif SETUP_DEPS:
        setup_deps()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-sl", "--setup-all", help="Setup everything [deps, configues]",action="store_true")
    parser.add_argument("-sd", "--setup-deps", help="Setup deps [pip packages]", action="store_true")
    parser.add_argument("-sc", "--setup-configues", help="Setup connfigues [spotify configue]", action="store_true")

    arguments = parser.parse_args()

    run(arguments)

