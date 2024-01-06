import os
from shazamio import Shazam
import time
from logs import logger_func

logger = logger_func(__name__)
st = time.time()
project_root = os.path.dirname(os.path.abspath(__file__))


def recognize_song(song_dir):
    try:

        command = fr'python "{project_root}/app.py" --path "{project_root}/{song_dir}" --rename'
        os.system(command)
        return True
    except Exception as e:
        logger.info(f"An error occurred: {e}")


async def metadata(song_dir):
    artist = song_title = ""
    try:
        shazam = Shazam()
        details = await shazam.recognize_song(song_dir)
        if 'track' in details:
            song_title = details['track']['title']
            artist = details['track']['subtitle']
            logger.info('Song found!')
            return artist, song_title
        else:
            logger.info('Song not found!')
            return artist, song_title
    except FileNotFoundError:
        logger.info("File not found.")
        return artist, song_title


async def get_metadata(song_dir):
    artist, song = await metadata(song_dir)
    return artist, song


