import data_grabber as DG
from downloader import *
from pytube import *
from mutagen.id3 import ID3, TIT2
from renamer import *
import os

#TEST_PLAYLIST_URL = "https://www.youtube.com/playlist?list=OLAK5uy_kq_gJdWJ9LUwgYzXMWeocvSyee4OqsvOQ"  # NFR

#
# WEIRD BUG check Dried Roses on Dragon New Warm Mountain--album title gets cut off at the end
#

# Change these constants to change what metadata is set
SET_TRACK_NUMBERS = True
SET_COVER_SOURCE = False
SET_COVER_ART = False

DOWNLOAD_COVERS = False

if __name__ == "__main__":
    # Gets inputs for the playlist to download and what folder to download to
    playlist_url = input("What is your desired YouTube playlist URL? ")
    output_path = input("What is your output folder's name? ")
    path = f"content/songs/"

    # Creates a list of all folders in desired path
    folders = output_path.split('/')
    
    # Runs through all the folders in the desired path
    for folder in folders:
        # Checks if path exists in content folder, if not, create new folder
        if not os.path.exists(f"{path}/"):
            os.mkdir(path)
        # Adds folder to complete output path
        path += f"{folder}/"

    # Only used if SET_TRACK_NUMBERS is set to True
    track_num = 1

    playlist = Playlist(playlist_url)
    #
    # Need to fix: NFR explicit not containing any data ?? Find another album that this happens on
    #
    for song_url in playlist.video_urls:
        dg = DG.DataGrabber(song_url)
        data = dg.get_data()
        file_name = rename(data["title"])
        
        print(f"Downloading...{file_name}")

        # Downloads covers if desired
        if DOWNLOAD_COVERS:
            download_cover(data["cover_src"], data["album"])
        
        download_song(song_url, path, file_name)

        audio = ID3()
        audio.add(TIT2(encoding=3, text=f"{data["title"]}"))  # THIS IS WORKING??? WRITING TITLE
        audio.save(f"{path}{file_name}.mp3")
        #audio.add_tags()

        print(file_name, "downloaded!\n")