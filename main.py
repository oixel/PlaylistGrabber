import data_handler as DH
from downloader import *
from renamer import *
from pytube import Playlist
import os

# Default: True -- Writes track number in MP3's metadata
# NOTE: Track number is representative of song's position in playlist 
# (Change the song's position in playlist to change the track number)
SET_TRACK_NUMBERS = True

# Default: True -- Writes track number (NOTE above) in filename before title (e.g. "01 Song Name.mp3")
SET_NUM_IN_FILENAME = True

# Default: True -- Embeds song's cover art into MP3 if available or generic filler drawing if not available
# NOTE: to make cover art be video thumbnail instead of cat drawing, uncomment code under line 69 of data_handler.py
SET_COVER_ART = True

# Default: True -- Sorts downloaded songs into paths equal to Artist/Album/
# NOTE: this is always set to True whenever downloading playlists from a .txt file
AUTO_SORT_SONGS = True

# Default: False -- Allows for custom artist and album to be embeded into metadata--overwriting found metadata
# NOTE: only affects Method 1 of inputting playlists URLs.
# NOTE: to set custom artist / album write "ARTIST[text]" and/or "ALBUM[text]" in the line above the playlist's URL
USE_CUSTOM_ARTIST = False
USE_CUSTOM_ALBUM = False

# Returns string in between two markers (if it exists) -- used to find ARTIST[] and ALBUM[] in .txt files
def get_substr(start_marker : str, end_marker : str, line : str) -> str | None:
    # Checks if marker even exists in main string
    if start_marker in line:
        # Gets positions of start and end of substring
        start = line.find(start_marker) + len(start_marker)
        end = line.find(end_marker, start)

        # If either start or end position of substring does not exist, custom data does not exist properly
        if start == -1 or end == -1:
            return None

        # Returns substring found in between the two positions
        return line[start:end]
    else:  # If start marker does not exist, then the substring does not either
        return None

if __name__ == "__main__":
    directory = os.path.dirname(__file__)

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
                artist = input(f"What is the custom ARTIST for playlist {i + 1}? (Leave blank for regular metadata) ")
                
                # Allows custom artist to be skipped for individual playlists by inputting nothing
                if artist != "":
                    custom_artists.append(artist)
                else:
                    custom_artists.append(None)
            else:  # Appends None for all values in custom_artists if not using custom artists
                custom_artists.append(None)
            
            # Gets custom album for current playlist if custom album is enabled
            if USE_CUSTOM_ALBUM:
                album = input(f"What is the custom ALBUM for playlist {i + 1}? (Leave blank for regular metadata) ")
                
                # Allows custom album to be skipped for individual playlists by inputting nothing
                if album != "":
                    custom_albums.append(album)
                else:
                    custom_albums.append(None)
            else:  # Appends None for all values in custom_albums if not using custom albums
                custom_albums.append(None)

            # Only asks for custom output path if auto sorting songs is turned off
            if not AUTO_SORT_SONGS:
                output_path = input(f"What is your output path for playlist {i + 1}? ")
                print()

                # Adds content/songs/ to the beginning of whatever desired path was inputted
                path = f"content/songs/{output_path}"

                # If path does not end with slash, add one to it
                if path[-1] != '/':
                    path += '/'
            else:
                # Specified output path is not needed if auto sorting since the path is generated using metadata
                path = None
            
            # Appends playlist url to recently created path
            playlist_paths.append((playlist_url, path))
    else:  # Called if reading playlist URLs from .txt file
        # Loops until the name of a existing .txt file is given
        while True:
            # Creates path from potential name of .txt file
            txt_name = input(f"What is your desired txt file's name (Exclude .txt)? ")
            txt_path = directory + "/content/url_txts/" + txt_name + ".txt"

            # Validates the existence (or lack thereof) of .txt file
            if not os.path.isfile(txt_path):
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
            if lines[i] == "END\n" or lines[i] == "END":  # Ends regardless if there are lines under END line
                break

            # If not a URL, skip this line
            if "https://www.youtube.com/playlist?list=" not in lines[i]:
                continue
            
            # Stores new path to overwrite autosort's Artist/Album (if PATH[text] is written in line above)
            new_path = get_substr("PATH[", "]", lines[i - 1])

            # Cleans up new path, if custom path exists
            if new_path != None:
                # Adds default folder path of content/songs/ to beginning of path
                new_path = f"content/songs/{new_path}"

                # If path does not end with slash, add one to it
                if new_path[-1] != '/':
                    new_path += '/' 
                    
            # Validates whether URL works
            try:
                validity_test = Playlist(lines[i])
                
                # If playlist exists, append to list of playlists with either the custom path found in the line above or None (so auto sort handles it)
                if validity_test:
                    playlist_paths.append((lines[i], new_path))
            except:  # If URL is broken, skip it
                continue
            
            # Stores custom artist (to overwrite metadata) if one is written in line above playlist URL
            new_artist = get_substr("ARTIST[", "]", lines[i - 1])
            custom_artists.append(new_artist)

            # Stores custom album (to overwrite metadata) if one is written in line above playlist URL
            new_album = get_substr("ALBUM[", "]", lines[i - 1])
            custom_albums.append(new_album)
    
    # Keeps track of what custom artist/album to embed in metadata for songs in current playlist
    custom_index = 0

    # Loops through all the URL / output path pairs in list
    for pair in playlist_paths:
        # Pulls values from the tuple into seperated variables
        playlist_url, desired_path = pair

        # Creates playlist object in pytube from URL
        playlist = Playlist(playlist_url)

        print(f"Now downloading all songs in {playlist.title}...\n")

        # Only used if set_track_number is set to True
        track_num = 1

        # Loops through URLs in playlist--downloading and writing metadata for each
        for song_url in playlist.video_urls:
            # Grabs data from YouTube video and stores it in DataGrabber object
            dh = DH.DataHandler(song_url)
            
            # Attempts to overwrite metadata using the values stored in the custom lists of custom values
            dh.overwrite_artist(custom_artists[custom_index])
            dh.overwrite_album(custom_albums[custom_index])
            
            # Stores filled out and (potentially) overwritten metadata dictionary into a dictionary
            data = dh.get_data()

            # Creates a appropriate file name with illegal characters and spaces removed
            file_name = rename(data["title"])

            # Writes tracknumber before song title in filename if desired
            if SET_NUM_IN_FILENAME:
                num_str = str(track_num) if track_num >= 10 else f"0{track_num}"
                file_name = f"{num_str} {file_name}"
            
            print(f"Downloading {file_name} by {data['artist']}...")

            # Overwrites output path to Artist/Album if auto sorting is turned on and custom path not desired in Method 2
            if AUTO_SORT_SONGS and desired_path == None:
                path_start = f"content/songs/{data['artist']}/"
                if data["album"] != "":
                    path = f"{path_start}{data['album']}/"
                else:  # If no metadata is found in YouTube video, place in UNORGANIZED folder under artist's name
                    path = f"{path_start}UNORGANIZED/"
            elif desired_path != None:  # Otherwise, if a custom path is desired, use that as output path instead
                path = desired_path

            # Ensures that path for song is allowed
            path = rename(path, True)

            # Attempts to download song using pytube, if it fails, skips over it
            if download_song(song_url, path, file_name) == False:
                # Removes song that failed to download
                os.remove(f"{directory}/{path}{file_name}.mp3")

                print("ERROR Resolved!")

                # Ensures the rest of the songs still have their correct track number
                track_num += 1

                continue
            
            # Writes metadata onto MP3s
            dh.write_data(f"{directory}/{path}", file_name, track_num, SET_TRACK_NUMBERS, SET_COVER_ART)

            # Increments track number in case it is being written in metadata
            track_num += 1
            
            print(f"{file_name} by {data['artist']} downloaded and written!\n")

        print(f"All songs in {playlist.title} have been downloaded!\n------------\n")

        # Increment index of custom artist/album
        custom_index += 1

    print("ALL playlists are done downloading! Enjoy your music! :)\n")