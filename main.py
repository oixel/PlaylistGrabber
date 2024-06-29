import data_handler as DH
from downloader import *
from renamer import *
from pytube import Playlist

# Change these constants to change what metadata is set
SET_TRACK_NUMBERS = True
SET_NUM_IN_FILENAME = True
SET_COVER_ART = True

# Change to true if album cover for song should be downloaded (if not already downloaded)
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
        # Pulls values from the tuple into seperated variables
        playlist_url, path = pair

        # Creates playlist object in pytube from URL
        playlist = Playlist(playlist_url)

        # Only used if set_track_number is set to True
        track_num = 1

        # Loops through URLs in playlist--downloading and writing metadata for each
        for song_url in playlist.video_urls:
            # Grabs data from YouTube video and stores it in DataGrabber object
            dh = DH.DataHandler(song_url)
            data = dh.get_data()

            # Creates a appropriate file name with illegal characters and spaces removed
            file_name = rename(data["title"])

            # Writes tracknumber before song title in filename if desired
            if SET_NUM_IN_FILENAME:
                num_str = str(track_num) if track_num >= 10 else f"0{track_num}"
                file_name = f"{num_str} {file_name}"
            
            print(f"Downloading {file_name} by {data["artist"]}...")

            # Downloads covers if desired
            if DOWNLOAD_COVERS:
                download_cover(data["cover_src"], data["album"])
            
            # Downloads song using pytube
            download_song(song_url, path, file_name)

            # Writes metadata onto MP3s
            dh.write_data(path, file_name, track_num, SET_TRACK_NUMBERS, SET_COVER_ART)

            # Increments track number in case it is being written in metadata
            track_num += 1
            
            print(file_name, "downloaded and written!\n")

        print(f"All songs in playlist downloaded!\n------------\n")

    print("ALL playlists done downloading! Enjoy :)\n")