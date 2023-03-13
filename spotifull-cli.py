#!/usr/bin/python3

import os
import sys
import time
import json
import argparse
import colorama
import requests
import threading

from pytube import YouTube, exceptions

API = "http://170.187.142.23:9898" # Change it to your own

def banner() -> None:
    """
        Spotifull CLI banner
    """
    print("""
\r        [37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37mQ[37mQ[37mQ[37mm[37m3[90ms[90m^[90m/[90m/[90m^[90m^[90m^[90m^[90m^[90m^[90m^[90m+[90m+[90m^[90mr[37my[37mS[37mQ[37mQ[37mQ[37m0[37m0[37m0[37m0[37m0[37m0
        [37m0[37m0[37m0[37m0[37m0[37m0[37m0[37mQ[37mQ[34m#[90mt[90m1[90m,[90m^[90mi[90mv[90m>[90mc[37mg[37mV[37mV[37mh[37mh[37mh[37mh[90m[[90m<[90mv[90m)[90m:[90m^[34m1[90m1[34mw[37mQ[37mQ[37m0[37m0[37m0[37m0
        [37m0[37m0[37m0[37m0[37m0[37m0[37mQ[37mD[37mh[90m)[90m)[90m[[90m![37mp[37mW[37mW[37mM[37mR[37mQ[37mQ[37mQ[37mQ[37mQ[37mQ[37mQ[37mQ[37mN[37mB[37mW[34mC[90m][90m][90m+[90m<[37md[37mM[37mQ[37m0[37m0[37m0
        [37m0[37m0[37m0[37m0[37m0[37m0[37mH[37mF[90m_[90m_[34m7[37mQ[37mQ[37mQ[37mQ[37mQ[37m8[37mO[37mk[37mY[37mY[37mY[37mY[37mY[37mY[37mk[37m@[37mQ[37mQ[37mQ[37mQ[37mQ[90m}[90m'[90m;[37md[37mD[37m0[37m0[37m0
        [37m0[37m0[37m0[37m0[37m0[37mQ[34mu[90m,[90m"[90m:[34mo[37mQ[33my[90mT[90mT[90mu[34m<[34m"[34m<[34mr[34ms[34mr[34mr[34ms[34mv[34m|[34mx[90mT[90mT[90mT[37mF[37mQ[90mI[90m;[90m|[90m,[34mw[37mQ[37m0[37m0
        [37m0[37m0[37m0[37m0[37mQ[37mQ[34mL[90m`[90m;[37my[34mw[90mc[34m>[34m)[34mr[34mI[36mw[36m3[36m6[36mg[36mg[36mg[36mg[36mg[36mq[36m5[36m#[34m}[34mr[34mi[34m>[90mc[37m3[34mJ[90m:[90m`[34mC[37mQ[37mQ[37m0
        [37m0[37m0[37m0[37m0[37mD[37mG[90me[90m|[90m"[90m^[34m"[34ml[34mj[36mp[36m5[36my[36mq[36mg[36mS[36mS[36mS[36mS[36mS[36mS[36mS[36mS[36my[36m5[36mS[36mp[34m7[34ml[90m+[90m^[90m|[90m|[90mj[37mP[37mK[37m0
        [37m0[37m0[37m0[37mQ[37mS[90m.[34m![34mT[36m2[90m,[34m;[34m![36m6[36mh[90mx[90m [36mf[36mg[36mS[36mS[36mS[36mS[36mS[36mS[36mS[36mF[90m_[90m\[36mg[36mg[36m6[34m?[34m-[90m|[36m2[34mT[34m![90m [37m6[37mQ
        [37m0[37m0[37m0[37mQ[37mg[90m:[34ml[34m?[36m5[90m^[34m;[34m?[36mp[36mg[34m?[90m|[36m2[36mS[36mS[36mS[36mS[36mS[36mS[36mS[36mg[36mq[90m>[34ms[36mS[36mS[36mp[34mI[90m_[90m)[36m5[34m}[34mc[90m:[37mq[37mQ
        [37m0[37m0[37m0[37mQ[37mh[90m:[34mx[34mI[34m#[90m,[34m^[34m?[36mp[36mS[36mS[36mS[36mg[36mg[36mS[36mS[36mS[36mS[36mS[36mh[36my[34mz[36m6[36mS[36mS[36mS[36mp[34mI[34m_[90m/[34m#[34m*[34m%[90m:[37mq[37mQ
        [37m0[37m0[37m0[37mQ[37mS[90m.[34m|[34mc[34m%[90m-[34m=[34m?[36mp[36mS[36mS[36mm[34m?[34m?[36m6[36mm[36mm[36mq[36mw[34m*[34m{[34m?[36m5[36mS[36mS[36mS[36mp[34m?[90m'[90m'[34mx[34mc[34m|[90m.[37mq[37mQ
        [37m0[37m0[37m0[37m0[37mH[37mP[90me[90m\[90m)[90m [34m^[34mI[36m3[36mg[36mS[36mq[36m#[34mj[90m%[90mv[90mv[90mv[34m{[36mT[36m3[36mh[36mS[36mS[36mS[36mg[36m6[34m?[34m_[90m`[90m\[90m\[90mj[37mG[37mH[37m0
        [37m0[37m0[37m0[37m0[37mQ[37mQ[37mR[37mW[37mD[90m{[34m<[34mv[34m?[36m#[36m5[36m6[36mS[36mS[36m6[36m6[36m6[36mp[36mm[36mh[36mg[36mg[36mS[36mq[36mq[36mF[34m7[34mi[90m|[90m][37mW[37mW[37mR[37mQ[37mQ[37m0
        [37m0[37m0[37m0[37m0[37m0[37m0[37mQ[37mQ[37mQ[37m0[37mb[90me[34m<[34m|[34mc[34m[[34m1[34me[36mJ[36m#[36mw[36m2[36m3[36m3[36mw[36m#[34mL[34m1[34mI[34m)[34m>[90mo[37mO[37m0[37mQ[37mQ[37mQ[37m0[37m0[37m0
        [37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37mQ[37mQ[37mQ[37mg[37mp[34m?[34m|[34m=[34m=[34m+[34m=[34m=[34m=[34m=[34m=[34m^[34m^[34m=[34m|[34mr[37mF[37md[37mQ[37mQ[37mQ[37m0[37m0[37m0[37m0[37m0[37m0
        [37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37mQ[37mQ[37mG[33m5[90m+[34m:[34mx[34ms[34mI[34me[34mo[34mt[34mi[90m,[90mi[37mp[37mX[37mQ[37mQ[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0
        [37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37mQ[37m5[90m][34m)[34m>[34m![36mF[36mh[36mh[36mh[36mV[36mw[34m![34m}[90m1[37my[37mQ[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37mQ[37mQ
        [37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37mQ[37mQ[33m2[90mj[34m\[34ml[34ml[34ml[34ml[34mr[90m1[90mJ[37mh[37mQ[37mQ[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37m0[37mN[37mK[37m8[39m
    \n\n""")

class Colors(object):
    def __init__(self) -> None:
        pass

    def blue(self):
        return colorama.Fore.BLUE
    
    def green(self):
        return colorama.Fore.GREEN

    def cyan(self):
        return colorama.Fore.CYAN
    
    def red(self):
        return colorama.Fore.RED
    
    def white(self):
        return colorama.Fore.WHITE
    
    def reset(self):
        return colorama.Fore.RESET

COLORS = Colors()

def check_api() -> bool:
    """
        Check if the API is running or not
    """
    try:
        requests.get(API)
        return True
    except:
        return False

def fetch_playlist_metadata(playlist_url: str) -> json:
    """
        Returns the metadata about the passed
        ```playlist_url```
    """
    try:
        REQ_CONTENT = requests.get(f"{API}/api/v1/get_playlist?playlist_url={playlist_url}")
        return REQ_CONTENT.json()
    except requests.exceptions.RequestException as error:
        return error

def download_music(download_url: str, youtube_url: str,save_path:str, artist_name: str, music_name: str) -> None:
    """
        Download music 
    """
    RETRY = 7

    print(f"\r{COLORS.blue()}   • {COLORS.white()}Downloading {COLORS.cyan()}{music_name}{COLORS.white()}...", end="")

    if download_url == None and youtube_url != None:
        YT_MUSIC = YouTube(youtube_url)
        try:
            YT_MUSIC.streams.get_highest_resolution().download(output_path=save_path, filename=f"{YT_MUSIC.streams[0].title}.mp3")
            print(f"{COLORS.green()} DONE")
        except exceptions.AgeRestrictedError:
            print(f"{COLORS.red()} FAILD")
        except exceptions.VideoUnavailable:
            print(f"{COLORS.red()} FAILD")

    elif download_url != None:
        try:
            REQ_CONTENT = requests.get(f"{API}{download_url}").content
            music_name = music_name.replace("/", "") if music_name.count("/") > 0 else music_name
            artist_name = artist_name.replace("/", "") if artist_name.count("/") > 0 else artist_name
            with open(f"{save_path}/{' - '.join([artist_name, music_name])}.mp3", "wb") as save_music:
                save_music.write(REQ_CONTENT)
            print(f"{COLORS.green()} DONE")
        except requests.exceptions.RequestException:
            print(f"{COLORS.red()} FAILD")
    elif youtube_url == None and download_url == None:
        print(f"{COLORS.red()} FAILD {COLORS.blue()}[{youtube_url = } , {download_url = }]")

def run(ARGS: argparse.ArgumentParser().parse_args) -> None:
    """
        Init CLI
    """
    global COLORS

    banner()
    if ("playlist_url" not in ARGS) and ("threads" not in ARGS):
        print(f"\r{COLORS.red()} [ ! ] {COLORS.white()} Use --help to see options")
        sys.exit(1)

    PLAYLIST_URL = ARGS.playlist_url
    SAVE_MUSIC_PATH = ARGS.save_path

    if not os.path.exists(SAVE_MUSIC_PATH):
        os.mkdir(SAVE_MUSIC_PATH)
    
    # Check the API
    print(f"\r{COLORS.cyan()} ==> {COLORS.white()}Checking the API...", end="")
    if check_api():
        print(f"{COLORS.green()} UP")
    else:
        print(f"{COLORS.red()} DOWN")
        sys.exit(1)

    # Requesting the metadata for the playlist
    print(f"\r{COLORS.cyan()} ==> {COLORS.white()}Requesting playlist metadata...", end="")
    PLAYLIST_METADATA = fetch_playlist_metadata(PLAYLIST_URL)
    
    if PLAYLIST_METADATA == requests.exceptions.RequestException:
        print(f"{COLORS.red()} FAILD")
        print(f"\r{COLORS.red()} [ ? ] {COLORS.white()}Requests exception occur : {PLAYLIST_METADATA}")
        sys.exit(1)
    
    print(f"{COLORS.green()} SUCCESS")

    print(f"{COLORS.green()} [ + ] {COLORS.white()}Start downloading music to `{COLORS.blue()}{SAVE_MUSIC_PATH}`")

    PLAYLIST_METADATA = PLAYLIST_METADATA["data"]

    for MUSIC in PLAYLIST_METADATA:
        ARTIST_NAME = MUSIC["artist_name"]
        MUSIC_NAME = MUSIC["name"]
        DOWNLOAD_URL = MUSIC["download_url"]
        YOUTUBE_URL = MUSIC["youtube_url"]
        
        download_music(DOWNLOAD_URL, YOUTUBE_URL, SAVE_MUSIC_PATH, ARTIST_NAME, MUSIC_NAME)

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description="Spotifull CLI")

    DOWNLOAD_SUB_ARG = PARSER.add_subparsers()

    DOWNLOAD = DOWNLOAD_SUB_ARG.add_parser("download")
    DOWNLOAD.add_argument("playlist_url", help="Spotify playlist url", nargs="?")
    DOWNLOAD.add_argument("save_path", help="Path to save the installed music", default="music", nargs="?")
    ARGS = PARSER.parse_args()

    run(ARGS)
