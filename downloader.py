import requests
from pytubefix import YouTube

# Takes in image source URL and downloads it at parameterized path
def download_cover(url, song_name) -> None:
    image_data = requests.get(url).content

    # Downloads album cover art in format of SongName.jpg in album_covers folder
    path =  f'content/album_covers/{song_name}.jpg'
    open(path, "wb").write(image_data)

# Downloads song at given url
def download_song(url, song_name) -> None:
    # Downloads an MP3 of the YouTube video audio from url to content/songs folder
    youtube = YouTube(url, use_oauth=True, allow_oauth_cache=True)

    stream = youtube.streams.get_audio_only()
    stream.download("content/songs/", f"{song_name}", mp3=True)