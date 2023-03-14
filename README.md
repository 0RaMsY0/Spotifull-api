<p align="center">
  <img src="https://github.com/0RaMsY0/Spotifull-api/blob/main/assets/images/spotifull_logo.png?raw=true" alt="Spotifull-api", width=300>
</p>

<div align="center">
   
  <p><h1>Spotifull-api</h1></p>

  <a href="">![status](https://img.shields.io/badge/status-development-red)</a>
  <a href="">![python version](https://img.shields.io/badge/python-%3E%3D%203.10-green)</a>
  <a href="">![issues](https://badges.hiptest.com:/bitbucket/issues/0RaMsY0/Spotifull-api?label=issues&style=plastic)</a>
  <a href="">![pull requests](https://img.shields.io/bitbucket/pr/0RaMsY0/Spotifull-api?color=red&style=plastic)</a>

</div>

# Why?

I was listening to my playlist one day when i realised that the number of ads that keeps on playing after aproximatly 5 to 10 tracks is increasing (i got 3 ads in a row), and i didn't like that ;), i did some research to find some tool to be able to download my playlist localy and i did found [spotdl](https://github.com/spotDL/spotify-downloader), it is very helpfull and i did used, but then i thaught i could maybe create something that is simalare, and that is how i ended up creating Spotifull-api.

# What is Spotifull-api?

In a nutshell, Spotifull-api is an API writen in python that uses the spotify API to fetch metada about a given playlist url and it have the ability to download this playlist and serve it to the end user and that for him to download it. With it you can create a service to download spotify playlist (by service i mean front-end).

# technology used

- **FastAPI** : API basically
- **pytube** : to search for the music on ***youtube*** in order to download it

# installation

To get started using Spotifull-api we are going to need a couple of dependencies, you can installe them by:
```bash
pip install -r requirements.txt
``` 
or you can use the [setup](https://github.com/0RaMsY0/Spotifull-api/blob/main/setup.py) script like so:
```bash
# to setup dependencies and configues use -sl
python setup.py -sl

# to download only the dependencies use -sd
python setup.py -sd

# to setup only the config files use -sd
python setup.py -sc
```

> **_NOTE:_**  Setting up the config files is important, you need to go to [spotify api dachboard](https://developer.spotify.com/dashboard/) and set it up then fill in with the information needed when running setup with -sc

# Usage

after we are done with the installation, we can now go ahead and start the Spotifull-api with:
```python
python main.py
```
> **_NOTE:_** Spotifull-API will be listening on all addresses 0.0.0.0 and on port 9898 by default by you can change that to your liking

Now you can navigate to http://localhost:9898/api/v1 and you should get something like this:
```bash
{
  "status code": 200
}
```

now go and get a playlist url in this case i will use [this one](https://open.spotify.com/playlist/7xmz5rpR2bSstByjr3vDId?si=6f910808f056436e), let send a GET requests to fetch the metadata for this playlist:
* using Curl:
    ```bash
    curl -X "GET" "http:/localhost:9898/api/v1/get_playlist?playlist_url=https://open.spotify.com/playlist/7xmz5rpR2bSstByjr3vDId?si=6f910808f056436e"
    ```
By default Spotifull-api will only fetch the metadata and return it like so:
```json
{
  "status code": 200,
  "session_id": "uBmCsbHoPT",
  "data": [
    {
      "name": "Yes Indeed",
      "spotify_url": "https://open.spotify.com/track/6vN77lE9LK6HP2DewaN6HZ",
      "publish_date": "2023-02-23T18:37:50Z",
      "artist_name": "Harder Than Ever",
      "cover_image": "https://i.scdn.co/image/ab67616d0000b2736cab41f8c84d6164976400d4",
      "preview_url": null,
      "youtube_url": "https://youtu.be/Z8IhZMJ3epU",
      "download_url": null
    },
  ]
}

```
> **_NOTE:_** "preview_url" sometimes can be ```null```

so if we want to download the music (server-side) and serve to the user or the client we will need to change the value of ```enable_local_download``` to ```true``` in **conf/api-conf.json**:
```json
{
    "enable_local_download": true
}
```
this will let Spotifull-api download the music presented in a playlist into the **data/<session_id>** folder, **session_id** is a random uid that is used to keep all the downloaded music clean and prevent conflict and also it prevent users/clients from accessing other users/clients playlist (they **can** access it if they know what the id), the **session_id** have an expiring time of 24h to if 24h passed the **session_id** will be deleted along side with music inside of **data/<session_id>**.

Now if we try to do a GET request again we will get:
```json
{
  "status code": 200,
  "session_id": "OtPwndQNSo",
  "data": [
    {
      "name": "Jefe (feat. Meek Mill)",
      "spotify_url": "https://open.spotify.com/track/1vw4TJRXkLuuJUtwh4UbYD",
      "publish_date": "2023-02-23T18:37:53Z",
      "artist_name": "DIME TRAP",
      "cover_image": "https://i.scdn.co/image/ab67616d0000b2731ea261daa852a6c5c465dff3",
      "preview_url": "https://p.scdn.co/mp3-preview/09e921aebcfffbaecdc9a2b17263a2b5d03fc3ed?cid=9eb1d0fd5b6f4b1d9a99da39da3879e6",
      "youtube_url": "https://youtu.be/NalbryU_EK0",
      "download_url": "/api/v1/get_music?music_id=sZiSEOFUHzbkxuALLQNr&session_id=OtPwndQNSo"
    },
  ]
}
```
Notice that "download_url" is not ```null``` and we actually get the url path to the current music in the playlist, we can use somthing like **mpv** to play it or **python** to download it.
> **_NOTE:_** "download_url" may sometimes be ```null`` so you may need to check for that if you are planning on writing a script to automate the installation process.

You can use the pre-writen [spotifull-cli.py](https://github.com/0RaMsY0/Spotifull-api/blob/main/spotifull-cli.py) to download your playlist. First you will need to have hosted the Spotifull-api (you may host it on a server or localy) then you need to change ```API``` variable inside of [spotifull-cli.py](https://github.com/0RaMsY0/Spotifull-api/blob/main/spotifull-cli.py) to your own url e.g ```http://0.0.0.0:9898```, then you can run:
``` bash
python spotifull-cli download <playlist_url> <path_to_save_music_to>
```
spotifull-cli.py is indepandent that means if you are on linux you can make it a command, like so:
```bash
chmod 777 spotifull-cli.py
sudo mv spotifull-cli /usr/bin/spotifull-cli
```
# CLI preview

<p align="center">
  <img src="https://github.com/0RaMsY0/Spotifull-api/blob/main/assets/images/cli-test.png?raw=true" alt="Spotifull-cli", width=500>
</p>

# Upcoming features

* Costum logging ✅ 
* Detect spaming and blocking them
* Improve the search on youtube feature to get better result

# API routes

|  route  |  description  |  query  |
|---------|---------------|---------|
|  /      | redirect to /api/v1 | None |
| /api/v1 | home route for the api | None |
| /api/v1/get_playlist | fetch a spotify playlist data | music_id |
| /api/v1/get_music | get a music that is already installed when calling ```/api/v1/get_playlist``` | music_id<br>session_id|
| /api/v1/server.log | returns the server/api log| None|

# Contributors ✨
Thanks go to these wonderful people
> **_NOTE_**: there aren't any contributors at this time but if you want to contribute you can, just look at issues and select one that you are capable of solving, or you can work on adding a feature.

# Feedback

I greatly appreciate any feedback you have on our project. you can either create an issue with yout feedback on something you want me to improve/add/fix or you can open a discution for it.