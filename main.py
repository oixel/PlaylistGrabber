import data_handler as DH
from downloader import *
from renamer import *
from pytube import Playlist
from os import path

# Default: True -- Writes track number in MP3's metadata
# NOTE: Track number is representative of song's position in playlist 
# (Change the song's position in playlist to change the track number)
SET_TRACK_NUMBERS = True

# Default: False -- Writes track number (as explained above) in filename before title (e.g. "01 Song Name.mp3")
SET_NUM_IN_FILENAME = False

# Default: True -- Embeds song's cover art into MP3 if available or generic filler drawing if not available
# NOTE: to make cover art be video thumbnail instead of cat drawing, uncomment code under line 69 of data_handler.py
SET_COVER_ART = True

# Default: False -- Sorts downloaded songs into paths equal to Artist/Album/
# NOTE: this is set to True whenever downloading playlists from a .txt file
AUTO_SORT_SONGS = False

# Default: False -- Allows for custom artist and album to be embeded into metadata when using Method 1
USE_CUSTOM_ARTIST = False
USE_CUSTOM_ALBUM = False

if __name__ == "__main__":
    # Loops until either a choice of 1 or 2 is made
    while True:
        try:
            print()
            print("How do you want to input playlist URLs?")
            print("1 - Input each URL individually")
            print("2 - Read from .txt file in url_txts folder")
            choice = int(input("Choice: "))
            print()

            if choice > 2 or choice < 1:
                raise ValueError
            
            break
        except ValueError:
            print("Please input either 1 or 2.\n")
    
    # Carries out futher setup depending on playlist URL input choice
    while True:
        if choice == 1:  # Gets desired count of playlists
            try:
                playlist_count = int(input("How many playlists are being downloaded? "))
                break
            except ValueError:
                print("Please input an integer.\n")
        else:  # Downloading from txt file auto sorts the songs by Artist/Album
            AUTO_SORT_SONGS = True
            break
    
    # Auto sorting songs conflicts with custom album and artist, so auto sorting disables customizing instead
    if AUTO_SORT_SONGS:
        USE_CUSTOM_ALBUM = False
        USE_CUSTOM_ARTIST = False

    # Stores tuples of format (YouTube link, output path)
    playlist_paths = []

    # Only filled if USE_CUSTOM_ARTIST is set to True
    custom_artists = []

    # Only filled if USE_CUSTOM_ALBUM is set to True
    custom_albums = []

    # If manually inputting each playlist URL, get every playlist URL
    if choice == 1:
        # Fills playlist_paths with URLs and output paths
        for i in range(playlist_count):
            # Loops until proper URL is pasted in
            while True:
                # Gets inputs for the playlist to download and what folder to download to
                playlist_url = input(f"What is your desired YouTube playlist URL for playlist {i + 1}? ")

                # Ensures that URL pasted is atleast somewhat a playlist URL
                if "https://www.youtube.com/playlist?list=" not in playlist_url:
                    print("Please enter proper YouTube playlist URL (e.g. includes https://www.youtube.com/playlist?list=)\n")
                    continue
                
                # Checks to see if playlist actually exists
                try:
                    validity_test = Playlist(playlist_url)
                    
                    # If playlist exists, move on to next part
                    if validity_test:
                        break
                except:
                    print("URL is broken, please input another!\n")
                    continue   
            
            # Gets custom artist for current playlist if custom artist is enabled
            if USE_CUSTOM_ARTIST:
                artist = input(f"What is the custom ARTIST for playlist {i + 1}? ")
                custom_artists.append(artist)
            
            # Gets custom album for current playlist if custom album is enabled
            if USE_CUSTOM_ALBUM:
                album = input(f"What is the custom ALBUM for playlist {i + 1}? ")
                custom_albums.append(album)

            # Only asks for custom output path if auto sorting songs is turned off
            if not AUTO_SORT_SONGS:
                output_path = input(f"What is your output path for playlist {i + 1}? ")
                print()
            else:
                # Specified output path is not needed if auto sorting since the path is generated using metadata
                output_path = ""
            
            # Adds content/songs/ to the beginning of whatever desired path was inputted
            path = f"content/songs/{output_path}"

            # If path does not end with slash, add one to it
            if path[-1] != '/':
                path += '/'
            
            # Appends playlist url to recently created path
            playlist_paths.append((playlist_url, path))
    else:  # Called if reading playlist URLs from .txt file

        # Loops until the name of a existing .txt file is given
        while True:
            # Creates path from potential name of .txt file
            txt_name = input(f"What is your desired txt file's name (Exclude .txt)? ")
            txt_path = "url_txts/" + txt_name + ".txt"

            # Validates the existence (or lack thereof) of .txt file
            if not path.isfile(txt_path):
                # Forces another loop if file does not exist
                print("Please input the name of a text file that exists in the url_texts folder.\n")
                continue
            
            # Only reached if file does exist
            print(f"Downloading playlists in {txt_name}.txt...\n")
            break
        
        # Creates a list of all lines in .txt file
        url_txt = open(txt_path, "r")
        lines = url_txt.readlines()

        # Loops through every line in .txt file and stores the working playlist URLs into playlist_paths
        for i in range(len(lines)):
            # Write "END" at desired end if you wish to write comments or something outside of checked loop
            if "END" in lines[i]:
                break

            # If not a URL, skip this line
            if "https://www.youtube.com/playlist?list=" not in lines[i]:
                continue

            # Validates whether URL works
            try:
                validity_test = Playlist(lines[i])
                
                # If playlist exists, append to list of playlists
                if validity_test:
                    playlist_paths.append((lines[i], ""))  # Has no specified path since path will be generated every song download
            except:  # If URL is broken, skip it
                continue
    
    # Keeps track of what custom artist/album to embed in metadata for songs in current playlist
    custom_index = 0

    # Loops through all the URL / output path pairs in list
    for pair in playlist_paths:
        # Pulls values from the tuple into seperated variables
        playlist_url, path = pair

        # Creates playlist object in pytube from URL
        playlist = Playlist(playlist_url)

        print(f"Now downloading all songs in {playlist.title}...\n")

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
  
            # Overwrites output path to Artist/Album if auto sorting is turned on
            if AUTO_SORT_SONGS:
                path_start = f"content/songs/{data["artist"]}/"
                if data["album"] != "":
                    path = f"{path_start}{data['album']}/"
                else:  # If no metadata is found in YouTube video, place in UNORGANIZED folder under artist's name
                    path = f"{path_start}UNORGANIZED/"

            # Downloads song using pytube
            download_song(song_url, path, file_name)

            # Sets custom artist/album to what was inputted at beginning if custom artist/album is enabled
            custom_artist = custom_artists[custom_index] if USE_CUSTOM_ARTIST else None
            custom_album = custom_albums[custom_index] if USE_CUSTOM_ALBUM else None
            
            # Writes metadata onto MP3s
            dh.write_data(path, file_name, track_num, SET_TRACK_NUMBERS, SET_COVER_ART, custom_artist, custom_album)

            # Increments track number in case it is being written in metadata
            track_num += 1
            
            print(f"{file_name} by {data["artist"]} downloaded and written!\n")

        print(f"All songs in {playlist.title} have been downloaded!\n------------\n")

        # Increment index of custom artist/album
        custom_index += 1

    print("ALL playlists are done downloading! Enjoy your music! :)\n")