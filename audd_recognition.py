import requests
import json
from dotenv import load_dotenv
import os
from logs import logger_func

logger = logger_func(__name__)
load_dotenv()


def recognize_song(song_dir):

    album_artist = artist_name = track_name = album_name = genre = release_date = ""
    try:

        data = {
            'api_token': os.getenv("API_TOKEN")
        }
        files = {
            'file': open(song_dir, 'rb')

        }
        result = requests.post("https://api.audd.io/", data=data, files=files)
        json_result = json.loads(result.text)
        artist_name = json_result['result']['artist']
        track_name = json_result['result']['title']
        logger.info(f"Successfully found song {artist_name}-{track_name}")
        return album_artist, artist_name, track_name, album_name, genre, release_date
    except Exception as e:
        logger.info(f"An error occurred: {e}")
        return artist_name, track_name
