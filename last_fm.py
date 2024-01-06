from dotenv import load_dotenv
import requests
import os
from unidecode import unidecode
from logs import logger_func

logger = logger_func(__name__)
load_dotenv()
api_key = os.getenv("API_KEY")


def download_coverart(artist, song_title):
    """
    Download the coverart from last_fm with the specified artist & song name
   :param artist: the name of the artist
    :param song_title: the name of the song
    :return: return successfully downloaded when the coverart has been downloaded
    """
    artist = artist.rstrip()
    song_title = song_title.rstrip()
    url = f"http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={api_key}&artist={artist}&track={song_title}&format=json"
    response = requests.get(url)

    album_artist = artist_name = track_name = album_name = genre = release_date = "Not available"
    if response.status_code == 200:
        data = response.json()
        if 'track' in data and 'album' in data['track'] and 'image' in data['track']['album']:
            artwork_url = data['track']['album']['image'][-1]['#text']
            if artwork_url:
                # Download the artwork here
                response = requests.get(artwork_url)
                if response.status_code == 200:
                    if 'track' in data and 'album' in data['track']:
                        # convert artists name & songs to ASCII for comparison
                        # e.g Christian Loffler should be equal to Christian Löffler
                        ascii_artist = unidecode(artist).upper()
                        ascii_song_title = unidecode(song_title).upper()

                        track_name = data['track']['name']
                        album_artist = data['track']['album']['artist']
                        if (ascii_artist in unidecode(album_artist).upper()) and (ascii_song_title in unidecode(track_name).upper()):
                            with open(f"{artist}_{song_title}_cover_art.jpg", 'wb') as f:
                                f.write(response.content)
                            logger.info(f"Downloaded artwork for {artist} by {song_title}")
                            return "Successfully downloaded"
                        else:
                            logger.info("Song not not found on last_fm")
                else:
                    logger.info(f"Failed to download artwork for {song_title} by {artist}")
                    return album_artist, artist_name, track_name, album_name, genre, release_date
            else:
                logger.info(f"No artwork found for {song_title} by {artist} on last.fm")
                return album_artist, artist_name, track_name, album_name, genre, release_date
        else:
            logger.info(f"No artwork found for {song_title} by {artist} on last.fm")
            return album_artist, artist_name, track_name, album_name, genre, release_date
    else:
        logger.info(f"Failed to fetch data for {song_title} by {artist} on last.fm")
        return album_artist, artist_name, track_name, album_name, genre, release_date


def get_metadata(artist, song_title):

    artist = artist.rstrip()
    song_title = song_title.rstrip()
    url = f"http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={api_key}&artist={artist}&track={song_title}&format=json"
    response = requests.get(url)
    album_artist = artist_name = track_name = album_name = genre = release_date = ""
    if response.status_code == 200:
        data = response.json()
        if 'track' in data and 'album' in data['track']:
            artist = artist.rstrip()
            song_title = song_title.rstrip()
            # convert artists name & songs to ASCII for comparison
            # e.g Christian Loffler should be equal to Christian Löffler
            ascii_artist = unidecode(artist).upper()
            ascii_song_title = unidecode(song_title).upper()

            track_name = data['track']['name']
            album_artist = data['track']['album']['artist']
            if (ascii_artist in unidecode(album_artist).upper()) and (ascii_song_title in unidecode(track_name).upper()):
                album_name = data['track']['album']['title']
                logger.info(f"Got {artist}-{song_title} metadata")
            else:
                logger.info(f"{artist}-{song_title} not not found on last_fm")
                artist_name = track_name = album_artist = ""
            return album_artist, artist_name, track_name, album_name, genre, release_date
        else:
            logger.info(f"Song not found for {song_title} by {artist} on last.fm")
            return album_artist, artist_name, track_name, album_name, genre, release_date
    else:
        logger.info(f"Failed to fetch data for {song_title} by {artist} on last.fm")
        return album_artist, artist_name, track_name, album_name, genre, release_date

