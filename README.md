# PlaylistGrabber
A set of Python scripts that takes a YouTube playlist link of songs, downloads them, and embeds their metadata.

# Getting Started
NOTE: You must have Python3 and pip already installed before following these steps.

1) Download .zip
2) Extract it to desired path
3) Open OS's terminal or the terminal inside IDE of choice
4) cd into PlaylistGrabber folder
5) run "pip install -r requirements.txt"
6) run "python -m main"

You are now all set up!

### ⭐ NOTE ⭐
On your first attempt to download anything, you will receive a message saying: 

- "Please open [ Google device link ] and input code ###-###-####".

Authorizing an account is necessary in order to install songs using the pytube library.

If you desire to download songs marked as explicit by YouTube, you must log in to an account with age registrictions turned off. Otherwise, explicit songs will be skipped by downloader

# Methods of Input
There are two ways to input YouTube playlist URLs and both may be useful in different scenarios.

1) Input each URL individually
2) Read the URLs stored in a .txt file

By default, songs in playlists with mostly full metadata (artist and album) are downloaded to a path that follows the format of "content/songs/Artist Name/Album Name/". However, this varies depending on what metadata is available under the video. If no artist's name is found, it substitutes with the video uploader's name instead. If no album name is found, there is no alternative data to work with, so it instead gets placed into a "UNORGANIZED" folder under the artist's (or uploader's) name.

Of course these paths can be overriden; however, the process of overriding depends on whether Method 1 or 2 is being used.

### Method 1: Inputting each URL individually
This method is better utilized when installing playlists once without concern of reusing the link again in the future. It skips the work of creating a .txt file and simply installs the playlists inputted instantly.

Output paths can be overrided by changing the settings of the following constants in main.py:

__NOTE__: Keeping AUTO_SORT_SONGS as True while using custom data will place songs in "content/songs/Custom Artist Name/ Custom Album Name/".

* AUTO_SORT_SONGS = (Default = True)
    - Turning this off will result in your desired output path being asked after inputting each URL.
* USE_CUSTOM_ARTIST = (Default = False)
    - Allows input at start that overwrites any artist or uploader names that are found.
* USE_CUSTOM_ALBUM = (Default = False)
    - Allows input at start that overwrites any found album names.

### Method 2: Reading from .txt
TO BE TYPED UP SOON...

# Additional Settings
Futher changes are able to be made to how the songs themselves are downloaded. Changing these settings alters the downloads regardless of what method is used to install the songs.

Universal Settings:
* SET_TRACK_NUMBERS (Default = True)
    - Writes spot of downloaded song in playlsit as track number in metadata.
* SET_NUM_IN_FILENAME = (Default = True)
    - Writes the track number in the filename of song (Example: 01 Song Name.mp3).
* SET_COVER_ART = (Default = True)
    - If a image is provided in song's YouTube description, embeds it as the song's cover art.
    - __NOTE__: If no song is found, it will instead embed [this silly cat I drew.](https://i.ibb.co/DDKn0JH/starcat.jpg)
      - If you wish to use a different default image, change the URL of DEFAULT_COVER_SOURCE in data_handler.py (Recommended to be 512x512 pixels).
      - Alternatively, if you desire songs with no found cover to be left blank, set DEFAULT_COVER_SOURCE in data_handler.py to None.
     
