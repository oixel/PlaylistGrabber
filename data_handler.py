import requests
from bs4 import BeautifulSoup as BS
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from io import BytesIO
from renamer import fix_unicode
from downloader import get_song

class DataHandler:
    # Used in checking whether found cover source is proper album cover art
    COVER_LINK_START = 'https://lh3.googleusercontent.com/'

    # Each marker represents the HTML that comes right before each specific piece of metadata
    COVER_MARKER = ',{"horizontalCardListRenderer":{"cards":[{"videoAttributeViewModel":{"image":{"sources":[{"url":"'
    SONG_MARKER = '"}]},"imageStyle":"VIDEO_ATTRIBUTE_IMAGE_STYLE_SQUARE","title":"'
    ARTIST_MARKER = '","subtitle":"'
    ALBUM_MARKER = '"secondarySubtitle":{"content":"'

    def __init__(self, url) -> None:
        # Stores URL of YouTube video for usage in set_filler()
        self.url = url

        # Creates a giant string of the entire HTML for the YouTube video's page.
        html = requests.get(url).content

        # Uses BeautifulSoup to parse through the HTML data and convert it to a "legible" string
        bs = BS(html, "html.parser")
        self.html = bs.prettify()[700000:]  # Everything before ~700000 does not include metadata info

        # Creates an empty dictionary to fill with metadata
        self.metadata = {}

        # Makes sure that first search for album cover starts at the beginning of HTML
        self.prev_end = 0

        self.create_data()

    # Takes marker and searches for it from the previous data's end character index to the end of the HTML
    # Returns: new point to search for next marker from and found data
    def find_data(self, marker, end_marker='"', is_cover_src = False) -> tuple[int, str]:
        # Sets offset to make sure that weird HTML data is not included in metadata information
        offset = len(marker)

        try:
            # Start search at last data's end and add offset of character count of marker to make sure it searches past marker
            start = self.html.index(marker, self.prev_end) + offset
            end = self.html.index(end_marker, start)  # " indicates the end of metadata value
            data = self.html[start:end]
            
            # Ensures that there is no indexing bug for a cover source that does not actually exists
            if data != None:
                if is_cover_src and self.COVER_LINK_START not in data:
                    raise
            
            # Only gets called if no error was raised
            new_start = end
        except:
            # If any error is raised, then found metadata is incorrect or non-existent
            new_start = self.prev_end
            data = None

        # Returns the value of the new start and the metadata that was found (or not found)
        return new_start, data

    # Alters the empty values in metadata to mirror YouTube video's information
    def set_filler(self) -> None:
        # Gets YouTube video's basic information utilizing pytube in downloader.py
        song = get_song(self.url)

        # If no album cover art is available, set cover to custom made starcat filler image
        if self.metadata["cover_src"] == None:
            self.metadata["cover_src"] = "https://i.ibb.co/DDKn0JH/starcat.jpg"

            # NOTE: Uncomment to utilize video's thumbnail instead of awesome starcat image
            # self.metadata["cover_src"] = song.thumbnail_url
        
        # If no song title is available, set title to YouTube video's title
        if self.metadata["title"] == None:
            self.metadata["title"] = song.title

        # If not artist name is available, set artist name to YouTube video's creator
        if self.metadata["artist"] == None:
            self.metadata["artist"] = song.author
        
        # Just set album to an empty string instead of None since there is no relevant info
        if self.metadata["album"] == None:
            self.metadata["album"] = ""

    # Pulls all desired metadata from self's HTML and stores it in internal dictionary
    def create_data(self) -> None:
        # Gets album cover's source
        self.prev_end, self.metadata["cover_src"] = self.find_data(self.COVER_MARKER, is_cover_src=True)
        
        # Gets song's title
        self.prev_end, self.metadata["title"] = self.find_data(self.SONG_MARKER, end_marker='","subtitle":"')

        # Gets artist's name
        # If there is a song title, include it in marker for more accurate finding
        if self.metadata["title"] != None:
            self.prev_end -= len(self.metadata["title"])
            artist_marker = f'{self.metadata["title"]}{self.ARTIST_MARKER}'
        else:
            artist_marker = self.ARTIST_MARKER
        self.prev_end, self.metadata["artist"] = self.find_data(artist_marker)

        # Gets album's name
        self.prev_end, self.metadata["album"] = self.find_data(self.ALBUM_MARKER)

        # Ensures that song does not leave with no information
        if None in self.metadata.values():
            self.set_filler()
        
        # Fixes weird glitch that reads ampersand as unicode by converting unicode to symbol
        if self.metadata["title"] != None:
            self.metadata["title"] = fix_unicode(self.metadata["title"])
        if self.metadata["artist"] != None:
            self.metadata["artist"] = fix_unicode(self.metadata["artist"])
        if self.metadata["album"] != None:
            self.metadata["album"] = fix_unicode(self.metadata["album"])

        return self.metadata

    # Returns currently stored metadata
    def get_data(self) -> dict:
        return self.metadata

    # Writes metadata into MP3 file
    def write_data(self, path, file_name, track_num, set_track_number, set_cover_art) -> None:
        # Creates an EasyID3 object and edits their metadata using mutagen
        audio = EasyID3()
        audio["title"] = f"{self.metadata['title']}"
        
        # Embeds scraped artist or custom artist (if overwriting occured) into MP3
        audio["artist"] = f"{self.metadata['artist']}"
        audio["albumartist"] = f"{self.metadata['artist']}"
        
        # Writes scraped album or custom album (if overwriting occured) into MP3
        audio["album"] = f"{self.metadata['album']}"

        # If track numbers are desired, write track number into metadata
        if set_track_number:
            audio["tracknumber"] = f"{track_num}"

        # Saves metadata into proper MP3 file
        audio.save(f"{path}{file_name}.mp3")

        # Only embeds album covers if it desired
        if set_cover_art:
            # Reads and store byte data for album cover image from image source's URL
            cont = requests.get(self.metadata['cover_src']).content
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

    # If a custom artist is desired for current playlist, overwrite the currently stored artist for this song
    def overwrite_artist(self, artist) -> None:
        if artist != None:
            self.metadata['artist'] = artist

    # If a custom album is desired for current playlist, overwrite the currently stored album for this song
    def overwrite_album(self, album) -> None:
        if album != None:
            self.metadata['album'] = album