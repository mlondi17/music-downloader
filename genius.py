import requests
import os
from dotenv import load_dotenv
import time
from unidecode import unidecode
from logs import logger_func

logger = logger_func(__name__)
st = time.time()
load_dotenv()

CLIENT_ID = os.getenv("GENIUS_CLIENT_ID")
CLIENT_SECRET = os.getenv("GENIUS_CLIENT_SECRET")


def authenticate_genius(client_id, client_secret):
    url = "https://api.genius.com/oauth/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(url, data=data)
    response_data = response.json()

    if "access_token" in response_data:
        return response_data["access_token"]
    else:
        logger.info("Authentication failed.")
        return None


def json_metadata(artist_name, song_title):
    access_token = authenticate_genius(CLIENT_ID, CLIENT_SECRET)
    artist_name = artist_name.rstrip()
    song_title = song_title.rstrip()

    # Search for the song on Genius
    url = f"https://api.genius.com/search?q={artist_name} {song_title}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    response_data = response.json()
    return response_data


def get_metadata(artist, song_title):
    album_artist = artist_name = track_name = album_name = genre = release_date = ""
    try:
        response_data = json_metadata(artist, song_title)
        if "response" in response_data:
            hits = response_data["response"]["hits"]
            if hits:
                song = hits[0]["result"]
                # convert artists name & songs to ASCII for comparison
                # e.g Christian Loffler should be equal to Christian Löffler
                ascii_artist = unidecode(artist).upper()
                ascii_song_title = unidecode(song_title).upper()

                song_full_title = song['full_title'].split("by")[0]
                artist_names = song['artist_names']
                if (ascii_artist in unidecode(artist_names).upper()) and (
                        ascii_song_title in unidecode(song_full_title).upper()):
                    album_artist = song['primary_artist']['name']

                    artist_name = song['artist_names']
                    release_date = song['release_date_components']['year']
                    track_name = song_title
                    if 'album' in song:
                        album_name = song['album']['name']
                else:
                    logger.info(f"{artist}-{song_title} not found on genius.")
                logger.info(f'{artist}-{song_title} metadata found')
                return album_artist, artist_name, track_name, album_name, genre, release_date

            else:
                logger.info(f"Song {artist}-{song_title} not found on Genius.")
                return album_artist, artist_name, track_name, album_name, genre, release_date
        else:
            logger.info("Failed to fetch data from Genius.")
            return album_artist, artist_name, track_name, album_name, genre, release_date
    except Exception as e:
        logger.info(f"An error occurred: {e} on genius")
        return album_artist, artist_name, track_name, album_name, genre, release_date


def download_coverart(artist, song_title):
    try:
        response_data = json_metadata(artist, song_title)
        if "response" in response_data:
            hits = response_data["response"]["hits"]

            if hits:
                song = hits[0]["result"]
                # convert artists name & songs to ASCII for comparison
                # e.g Christian Loffler should be equal to Christian Löffler
                ascii_artist = unidecode(artist).upper()
                ascii_song_title = unidecode(song_title).upper()

                song_full_title = song['full_title'].split("by")[0]
                artist_names = song['artist_names']
                if (ascii_artist in unidecode(artist_names).upper()) and (
                        ascii_song_title in unidecode(song_full_title).upper()):
                    if 'song_art_image_url' in hits[0]['result']:
                        coverart = hits[0]['result']['song_art_image_url']

                    else:

                        coverart = hits[0]['result']['header_image_url']

                    response = requests.get(coverart)
                    if response.status_code == 200:
                        file_name = f"{artist}_{song_title}_cover_art.jpg"
                        with open(file_name, "wb") as f:
                            f.write(response.content)
                        logger.info(
                            f'Successfully downloaded cover art for {artist}-{song_title}'
                        )
                        return "Successfully downloaded"
                    else:
                        logger.info(f"Failed to download Cover Art for {artist}-{song_title}")
                else:
                    logger.info(f"{artist}-{song_title} not found on genius")
            else:
                logger.info(f"Details about {artist}-{song_title} not found on genius")
        else:
            logger.info(f"{artist}-{song_title} not found on genius")
    except Exception as e:
        logger.info(f"An error occurred: {e} on genius")

