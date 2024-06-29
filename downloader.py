from pytubefix import YouTube
from pydub import AudioSegment

# Utilizes pydubs' AudioSegment class to convert fake MP3 downloaded from YouTube audio to recognizable MP3 file
def convert_to_proper_mp3(path) -> None:
    AudioSegment.from_file(path).export(path, format="mp3")

# Downloads song at given url
def download_song(url, path, song_name) -> None:
    # Downloads an MP3 of the YouTube video audio from url to content/songs folder
    youtube = YouTube(url, use_oauth=True, allow_oauth_cache=True)

    # Downloads audio of video as fake MP3 file
    stream = youtube.streams.get_audio_only()
    stream.download(f"{path}", f"{song_name}", mp3=True)

    # Converts fake MP3 from video audio to proper MP3 file
    convert_to_proper_mp3(f"C:/Users/oycel/Code/Projects/PlaylistGrabber/{path}{song_name}.mp3")

# Returns YouTube object to access basic video information for filler metadata
def get_song(url) -> None:
    return YouTube(url, use_oauth=True, allow_oauth_cache=True)