import musicbrainzngs
from unidecode import unidecode
from logs import logger_func

logger = logger_func(__name__)


def download_coverart(artist, song_title):
    artist = artist.rstrip()
    song_title = song_title.rstrip()
    try:
        musicbrainzngs.set_useragent('TheRecordIndustry.io', '0.1')

        search_track = musicbrainzngs.search_releases(query=song_title, artist=artist)
        if 'release-list' in search_track and search_track['release-list']:
            track_id = search_track['release-list'][0]['id']
            recording = search_track['release-list'][0]
            # convert artists name & songs to ASCII for comparison
            # e.g Christian Loffler should be equal to Christian Löffler
            ascii_artist = unidecode(artist).upper()
            ascii_song_title = unidecode(song_title).upper()

            track_name = recording['title'].replace(".", "")
            artist_name = recording['artist-credit-phrase']
            if (ascii_artist in unidecode(artist_name).upper()) and (ascii_song_title in unidecode(track_name).upper()):
                cover_art = musicbrainzngs.get_image(track_id, coverid='front', size='500')

                file_name = f"{artist}_{song_title}_cover_art.jpg"
                with open(file_name, "wb") as f:
                    f.write(cover_art)
                logger.info(f"Successfully downloaed coverart for {artist}-{song_title}")
                return "Successfully downloaded"
            else:
                logger.info(f'{artist}-{song_title} not found')

        else:
            logger.info(f'Cover art not found musicbrainzngs for {artist}-{song_title}')
    except musicbrainzngs.musicbrainz.ResponseError:
        logger.info(f"{artist}-{song_title} not found on musicbrainzngs.")
    except Exception as e:
        logger.info(f"An error occurred: {e}")


def get_metadata(artist, song_title):
    artist = artist.rstrip()
    song_title = song_title.rstrip()
    album_artist = artist_name = track_name = album_name = genre = release_date = ""
    try:
        musicbrainzngs.set_useragent('TheRecordIndustry.io', '0.1')

        search_track = musicbrainzngs.search_recordings(query=song_title, artist=artist)
        if 'recording-list' in search_track and search_track['recording-list']:
            recording = search_track['recording-list'][0]
            # convert artists name & songs to ASCII for comparison
            # e.g Christian Loffler should be equal to Christian Löffler
            ascii_artist = unidecode(artist).upper()
            ascii_song_title = unidecode(song_title).upper()

            track_name = recording['title'].replace(".", "")
            artist_name = recording['artist-credit-phrase']
            if (ascii_artist in unidecode(artist_name).upper()) and (ascii_song_title in unidecode(track_name).upper()):
                if 'title' in recording['release-list'][0]['release-group']:
                    album_name = recording['release-list'][0]['release-group']['title'].replace(".", "")

                else:
                    album_name = ""

                if 'artist-credit-phrase' in recording['release-list'][0]:
                    album_artist = recording['release-list'][0][
                        'artist-credit-phrase']
                else:
                    album_artist = artist

                if 'date' in recording['release-list']:
                    release_date = recording['release-list'][0]['date'].split("-")[0]
                logger.info("The song metadata found")
            else:
                track_name = artist_name = ""
                logger.info(f"The song of {artist}-{song_title} found doesn't match the required song.")
            return album_artist, artist_name, track_name, album_name, genre, release_date

        else:
            logger.info(f'The recording list of the song {artist}-{song_title} is not found')
            return album_artist, artist_name, track_name, album_name, genre, release_date

    except musicbrainzngs.musicbrainz.ResponseError:
        logger.info(f"Song {artist}-{song_title} not found")
        return album_artist, artist_name, track_name, album_name, genre, release_date
    except Exception as e:
        logger.info(f"An error occurred: {e}")
        return album_artist, artist_name, track_name, album_name, genre, release_date
