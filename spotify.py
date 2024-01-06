import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
from unidecode import unidecode
import subprocess
from logs import logger_func

load_dotenv()
client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                                                      client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"))
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

logger = logger_func(__name__)


def download_coverart(artist, song_title):
    artist = artist.rstrip()
    song_title = song_title.rstrip()
    try:
        query = f"track:{song_title} artist:{artist}"
        results = sp.search(query, limit=1, market="GB")
        if results['tracks']['items']:
            track_info = results['tracks']['items'][0]
            # convert artists name & songs to ASCII for comparison
            # e.g Christian Loffler should be equal to Christian Löffler
            ascii_artist = unidecode(artist).upper()
            ascii_song_title = unidecode(song_title).upper()

            artist_name = ', '.join([artist['name'] for artist in track_info['artists']])
            track_name = track_info['name']

            if ascii_artist in unidecode(artist_name).upper() and ascii_song_title in unidecode(track_name).upper():

                cover_art_url = track_info['album']['images'][0]['url']

                # Download the cover art
                response = requests.get(cover_art_url)

                if response.status_code == 200:
                    # Save the cover art image to a file
                    file_name = f"{artist}_{song_title}_cover_art.jpg"
                    with open(file_name, "wb") as f:
                        f.write(response.content)
                    logger.info("Successfully downloaded coverart")
                    return "Successfully downloaded"
                else:
                    logger.info(f"Failed to download Cover Art for {artist}-{song_title}")
            else:
                logger.info(f"The requested song {artist}-{song_title} couldn't be found on Spotify.")
        else:
            logger.info(f"Song {artist}-{song_title} not found on Spotify.")

    except Exception as e:
        logger.info(f"An error occurred: {e} ")


def get_metadata(artist, song_title):
    artist = artist.rstrip()
    song_title = song_title.rstrip()
    album_artist = artist_name = track_name = album_name = genre = release_date = ""
    try:
        # query = f"track:{song_title} artist:{artist}"
        query = 'https://api.spotify.com/v1/search?type=track&q=year:1958%20genre:"classical"&limit=50'
        results = sp.search(query, limit=1)

        if results['tracks']['items']:
            track_info = results['tracks']['items'][0]

            # convert artists name & songs to ASCII for comparison
            # e.g Christian Loffler should be equal to Christian Löffler
            ascii_artist = unidecode(artist).upper()
            ascii_song_title = unidecode(song_title).upper()

            artist_name = ', '.join([artist['name'] for artist in track_info['artists']])
            track_name = track_info['name']

            if ascii_artist in unidecode(artist_name).upper() and ascii_song_title in unidecode(track_name).upper():
                if track_info['album']['album_type'] == "single":
                    album_name = 'Single'
                else:
                    album_name = track_info['album']['name']
                album_artist = track_info['album']['artists'][0]['name']
                release_date = track_info['album']['release_date'].split("-")[0]
                logger.info("found song metadata.")
            else:
                artist_name = track_name = ""
            return album_artist, artist_name, track_name, album_name, genre, release_date

        else:
            return album_artist, artist_name, track_name, album_name, genre, release_date
    except Exception as e:
        logger.info(f"An error occurred: {e}")
        return album_artist, artist_name, track_name, album_name, genre, release_date


def download_song(artist_name, song_name):
    try:
        change_to = "{artist}_{title}.mp3"
        cmd = f'spotdl --output "{change_to}"  "{artist_name} {song_name}"'
        subprocess.call(cmd, shell=True)
        return True
    except Exception as e:
        logger.info(f"An error occurred: {e} ")


