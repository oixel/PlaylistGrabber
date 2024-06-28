import data_grabber as DG
from downloader import *
from renamer import *
from pytube import *
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from io import BytesIO

#TEST_PLAYLIST_URL = "https://www.youtube.com/playlist?list=OLAK5uy_kq_gJdWJ9LUwgYzXMWeocvSyee4OqsvOQ"  # NFR

#
# WEIRD BUG check Dried Roses on Dragon New Warm Mountain--album title gets cut off at the end
#

# Change these constants to change what metadata is set
SET_TRACK_NUMBERS = True
SET_COVER_SOURCE = False
SET_COVER_ART = True

DOWNLOAD_COVERS = False

if __name__ == "__main__":
    # Loops until a proper integer is given
    while True:
        try:
            playlist_count = int(input("How many playlists are being downloaded? "))
            break
        except ValueError:
            print("Please input an integer.")

    # Stores tuples of format (YouTube link, output path)
    playlist_paths = []

    # Fills playlist_paths with URLs and output paths
    for i in range(playlist_count):
        # Gets inputs for the playlist to download and what folder to download to
        playlist_url = input(f"What is your desired YouTube playlist URL for playlist {i + 1}? ")
        output_path = input(f"What is your output path for playlist {i + 1}? ")
        
        # Adds content/songs/ to the beginning of whatever desired path was inputted
        path = f"content/songs/{output_path}"

        # If path does not end with slash, add one to it
        if path[-1] != '/':
            path += '/'
        
        # Appends playlist url to recently created path
        playlist_paths.append((playlist_url, path))

    # Loops through all the URL / output path pairs in list
    for pair in playlist_paths:
        # Only used if SET_TRACK_NUMBERS is set to True
        track_num = 1

        # Pulls values from the tuple into seperated variables
        playlist_url, path = pair

        # Creates playlist object in pytube from URL
        playlist = Playlist(playlist_url)

        # Loops through URLs in playlist--downloading and writing metadata for each
        for song_url in playlist.video_urls:
            # Grabs data from YouTube video and stores it in DataGrabber object
            dg = DG.DataGrabber(song_url)
            data = dg.get_data()

            # Creates a appropriate file name with illegal characters and spaces removed
            file_name = rename(data["title"])
            
            print(f"Downloading {file_name} by {data["artist"]}...")

            # Downloads covers if desired
            if DOWNLOAD_COVERS:
                download_cover(data["cover_src"], data["album"])
            
            # Downloads song using pytube
            download_song(song_url, path, file_name)

            # Creates an EasyID3 object and edits their metadata using mutagen
            audio = EasyID3()
            audio["title"] = f"{data["title"]}"
            audio["artist"] = f"{data["artist"]}"
            audio["albumartist"] = f"{data["artist"]}"
            audio["album"] = f"{data["album"]}"

            # If track numbers are desired, write track number into metadata and increment track number
            if SET_TRACK_NUMBERS:
                audio["tracknumber"] = f"{track_num}"
                track_num += 1

            # Saves metadata into proper MP3 file
            audio.save(f"{path}{file_name}.mp3")

            # Only embeds album covers if it desired
            if SET_COVER_ART:
                # Reads and store byte data for album cover image from image source's URL
                cont = requests.get(data["cover_src"]).content
                image_bytes = BytesIO(cont).read()

                # Creates an ID3 object for current song (EasyID3 does not support embedding album art)
                id3 = ID3(f"{path}{file_name}.mp3")
                
                # Embeds image byte data into front cover metadata tag
                id3["APIC"] = APIC(
                    encoding = 3,
                    mime = "image/jpeg",
                    type = 3,
                    desc = u'Cover',
                    data = image_bytes
                )

                # Saves new image data into MP3's ID3 metadata tags
                id3.save()
            
            print(file_name, "downloaded and written!\n")

        print(f"All songs in playlist downloaded!\n------------\n")

    print("ALL playlists done downloading! Enjoy :)")