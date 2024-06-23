import data_grabber as DG
from downloader import *
from pytube import *
import taglib
from io import BytesIO
import eyed3
from eyed3.id3.frames import ImageFrame
from renamer import *

#TEST_PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLvsYXqtYjMYfQ4gz7lC3UKa2DNsnlIKRM"  # Suki - I Can't Let Go
#TEST_PLAYLIST_URL = "https://www.youtube.com/playlist?list=OLAK5uy_kq_gJdWJ9LUwgYzXMWeocvSyee4OqsvOQ"  # NFR
#TEST_PLAYLIST_URL = "https://www.youtube.com/watch?v=1RKqOmSkGgM&list=PL2fTbjKYTzKcb4w0rhNC76L-MER585BJa"  # MM_Test
#TEST_PLAYLIST_URL = "https://www.youtube.com/watch?v=6S20mJvr4vs&list=PLRwfuN7siOr7p044Iw_7jfEhGPgfVdST-"  # IGOR
TEST_PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLfiMjLyNWxebu5tK9xUbPKcVeVpOwc8QI"  # CMIYGL

# Change these constants to change what metadata is set
SET_TRACK_NUMBERS = True
SET_COVER_SOURCE = True
SET_COVER_ART = False

DOWNLOAD_COVERS = False

if __name__ == "__main__":
    # Only used if SET_TRACK_NUMBERS is set to True
    track_num = 1

    playlist = Playlist(TEST_PLAYLIST_URL)
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
        
        download_song(song_url, file_name)

        # Writes basic info into MP3's ID3 metadata
        with taglib.File(f"content/songs/{file_name}.mp3", save_on_exit=True) as mp3:
            mp3.tags["TITLE"] = [data["title"]]
            mp3.tags["ALBUM"] = [data["album"]]
            mp3.tags["ARTIST"] = [data["artist"]]

            # Optional tags   
            if SET_TRACK_NUMBERS:
                mp3.tags['TRACKNUMBER'] = [f"{track_num}"]
                track_num += 1
            if SET_COVER_SOURCE:
                mp3.tags["COVER_SOURCE"] = [data["cover_src"]]

        if SET_COVER_ART:
            # Reads and store byte data for album cover image
            cont = requests.get(data["cover_src"]).content
            image_bytes = BytesIO(cont).read()

            # Writes image data to mp3 file and saves it if file can be read by eyed3
            eyed3_mp3 = eyed3.load(f"content/songs/{file_name}.mp3")
            if eyed3_mp3 != None:
                eyed3_mp3.tag.images.set(ImageFrame.FRONT_COVER, image_bytes, "image/jpeg")
                eyed3_mp3.tag.save(version=eyed3.id3.ID3_V2_4)

        print(file_name, "downloaded and written!\n")