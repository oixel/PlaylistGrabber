# PlaylistGrabber
A set of Python scripts that takes a YouTube playlist link of songs, downloads them, and embeds their metadata.

# Getting Started
NOTE: You must have Python3 and pip already installed before following these steps.

1) Download .zip
2) Extract it to desired path
3) Open OS's terminal or the terminal inside IDE of choice
4) cd into PlaylistGrabber folder
5) run "python -m main"

You are now all set up!

### ⭐ NOTE ⭐
When you attempt to download anything, you will receive a message saying: 

- "Please open [ Google device link ] and input code ###-###-####".

If you desire to download songs marked as explicit by YouTube, you must log in to an account with age registrictions turned off. Otherwise, explicit songs will be skipped by downloader

# Methods of Input & Settings
There are two ways to input YouTube playlist URLs and both may be useful in different scenarios. Along with this,

1) Input each URL individually
2) Read the URLs stored in a .txt file

### Method 1: Inputting each URL individually
This method is better utilized when installing playlists once without concern of reusing the link again in the future. It skips the work of creating a .txt file and simply installs the playlists inputted instantly. 

#### Settings
By default, manually inputting playlists on PlaylistGrabber organizes the downloaded songs in the same way as Method 2. However, changing the constants at the top of main.py can grant you more freedom in the outputs and output locations.

These settings are as follows:
* SET_TRACK_NUMBERS (Default = True)
    - Writes spot of downloaded song in playlsit as track number in metadata.
* SET_NUM_IN_FILENAME = (Default = True)
    - Writes the track number in the filename of song (Example: 01 Song Name.mp3).
* SET_COVER_ART = (Default = True)
    - If a image is provided in song's YouTube description, embeds it as the song's cover art.
    - __NOTE__: If no song is found, it will instead embed [this silly cat I drew.](https://i.ibb.co/DDKn0JH/starcat.jpg)
      - If you desire the default image to be something different, change the URL of DEFAULT_COVER_SOURCE in data_handler.py.
      - Alternatively, if you desire songs with no found cover to be left blank, set DEFAULT_COVER_SOURCE to None.
* AUTO_SORT_SONGS = (Default = True)
* USE_CUSTOM_ARTIST = (Default = False)
* USE_CUSTOM_ALBUM = (Default = False))

