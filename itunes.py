import requests
from unidecode import unidecode
from logs import logger_func

logger = logger_func(__name__)

def download_coverart(artist, song_title):

    artist = artist.rstrip()
    song_title = song_title.rstrip()
    url = f"https://itunes.apple.com/search?term={artist}+{song_title}&entity=song"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            result = data['results'][0]
            # convert artists name & songs to ASCII for comparison
            # e.g Christian Loffler should be equal to Christian Löffler
            ascii_artist = unidecode(artist).upper()
            ascii_song_title = unidecode(song_title).upper()
            artist_name = result['artistName']
            track_name = result['trackName']
            if (ascii_artist in unidecode(artist_name).upper()) and (ascii_song_title in unidecode(track_name).upper()):
                artwork_url = result.get('artworkUrl100')
                if artwork_url:
                    artwork_url = artwork_url.replace('100x100bb.jpg', '1000x1000bb.jpg')
                    response = requests.get(artwork_url)
                    if response.status_code == 200:
                        with open(f"{artist}_{song_title}_cover_art.jpg", 'wb') as f:
                            f.write(response.content)
                        logger.info(f"Successfully downloaded coverart for {artist}-{song_title}")
                        return "Successfully downloaded"
                    else:
                        logger.info(f"Failed to download artwork for {artist} by {song_title} on itunes")
                else:
                    logger.info(f"No artwork found for {artist} by {song_title} on itunes")
            else:
                logger.info("{artist}-{song_title} not found on itunes.")
        else:
            logger.info(f"No results found for {artist} by {song_title} on itunes")
    else:
        logger.info(f"Failed to fetch data for {artist} by {song_title} on itunes")


def get_metadata(artist, song_title):

    artist = artist.rstrip()
    song_title = song_title.rstrip()
    url = f"https://itunes.apple.com/search?term={artist}+{song_title}&entity=song"
    album_artist = artist_name = track_name = album_name = genre = release_date = ""
    try:

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if 'results' in data and len(data['results']) > 0:
                result = data['results'][0]
                # convert artists name & songs to ASCII for comparison
                # e.g Christian Loffler should be equal to Christian Löffler
                ascii_artist = unidecode(artist).upper()
                ascii_song_title = unidecode(song_title).upper()

                artist_name = result['artistName']
                track_name = result['trackName']
                if (ascii_artist in unidecode(artist_name).upper()) and (
                        ascii_song_title in unidecode(track_name).upper()):

                    release_date = result['releaseDate'].split("-")[0]
                    genre = result['primaryGenreName']
                    if "Single" in result['collectionName']:
                        album_name = "Single"
                    else:
                        album_name = result['collectionName']
                    album_artist = artist_name
                    logger.info("Got song metadata")

                else:
                    artist_name = track_name = ""
                return album_artist, artist_name, track_name, album_name, genre, release_date
            else:
                return album_artist, artist_name, track_name, album_name, genre, release_date

        else:
            logger.info(f"Failed to fetch data for {artist} by {song_title} on itunes")
            return album_artist, artist_name, track_name, album_name, genre, release_date

    except Exception as e:
        logger.info(f"An error occurred: {e}")
        return album_artist, artist_name, track_name, album_name, genre, release_date


