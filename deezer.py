import requests
from unidecode import unidecode

endpoint = "/search/track"
base_url = "https://api.deezer.com"
from logs import logger_func

logger = logger_func(__name__)


def download_coverart(artist, song_title):
    artist = artist.rstrip()
    song_title = song_title.rstrip()
    params = {
        "q": f"artist:'{artist}' track:'{song_title}'",
        "limit": 1
    }

    response = requests.get(base_url + endpoint, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'data' in data and len(data['data']) > 0:
            track = data['data'][0]
            # convert artists name & songs to ASCII for comparison
            # e.g Christian Loffler should be equal to Christian Löffler
            ascii_artist = unidecode(artist).upper()
            ascii_song_title = unidecode(song_title).upper()

            track_name = track['title_short']
            artist_name = track['artist']['name']
            if (ascii_artist in unidecode(artist_name).upper()) and (ascii_song_title in unidecode(track_name).upper()):
                if 'album' in track:
                    album_image_url = track['album']['cover_xl']  # Using 'cover_xl' for a larger image
                    if album_image_url:
                        # Download the album image here
                        response = requests.get(album_image_url)
                        if response.status_code == 200:
                            coverart_name = f"{artist}_{song_title}_cover_art.jpg"
                            with open(coverart_name, 'wb') as f:
                                f.write(response.content)

                            return "Successfully downloaded"
                        else:
                            logger.info(f"Failed to download image for '{song_title}' by {artist}")
                    else:
                        logger.info(f"No album image found for '{song_title}' by {artist}")
                else:
                    logger.info(f"Album for {artist}-{song_title} not found on deezer.")
            else:
                logger.info(f"{artist}-{song_title} not found on deezer.")
        else:
            logger.info(f"No tracks found by {artist} with '{song_title}' in the title on deezer.")
    else:
        logger.info(f"Failed to fetch track data for '{song_title}' by {artist} on deezer")


def get_metadata(artist, song_name):
    artist = artist.rstrip()
    song_name = song_name.rstrip()
    params = {
        "q": f"artist:'{artist}' track:'{song_name}'"
    }
    url = f"{base_url}{endpoint}"

    album_artist = artist_name = track_name = album_name = genre = release_date = ""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        data = response.json()
        if 'data' in data and len(data['data']) > 0:
            track = data['data'][0]

            # convert artists name & songs to ASCII for comparison
            # e.g Christian Loffler should be equal to Christian Löffler
            ascii_artist = unidecode(artist).upper()
            ascii_song_title = unidecode(song_name).upper()

            track_name = track['title_short']
            artist_name = track['artist']['name']
            if (ascii_artist in unidecode(artist_name).upper()) and (ascii_song_title in unidecode(track_name).upper()):
                if track['album']['title'] == track_name:
                    album_name = "Single"
                else:
                    album_name = track['album']['title']
                if 'release_date' not in track['album']:
                    release_date = ""
                else:
                    release_date = track['album']['release_date']
                genre = ""
                album_artist = artist_name
            else:
                track_name = artist_name = ""
            logger.info("Got metadata from deezer")
            return album_artist, artist_name, track_name, album_name, genre, release_date

        else:
            logger.info(f"Song not found for '{artist}' by {song_name} on deezer")
            return album_artist, artist_name, track_name, album_name, genre, release_date

    except requests.exceptions.RequestException as e:
        logger.info(f"Failed to fetch data for '{song_name}' by {artist}: {str(e)} on deezer")
        return album_artist, artist_name, track_name, album_name, genre, release_date

    except Exception as e:
        logger.info(f"An error occurred: {e}")
