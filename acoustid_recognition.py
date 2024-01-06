from dotenv import load_dotenv
import os
import acoustid
from logs import logger_func

load_dotenv()

api_key = os.getenv("ACOUST_ID_API_KEY")

logger = logger_func(__name__)


def recognize_song(file_path):
    artist_name = track_name = ""
    try:
        for score, recording_id, title, artist in acoustid.match(api_key, file_path):
            artist_name = artist
            track_name = title
        return artist_name, track_name

    except acoustid.NoBackendError:
        logger.info("Chromaprint library or fpcalc command-line tool cannot be found.")
        return artist_name, track_name
    except acoustid.FingerprintGenerationError:
        logger.info("No match is found on the server")
        return artist_name, track_name
    except acoustid.WebServiceError:
        logger.info("Audio can't be decoded")
        return artist_name, track_name
    except Exception as e:
        logger.info(f"An error occurred: {e}")
        return artist_name, track_name
