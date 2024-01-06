import eyed3
from eyed3.id3.frames import ImageFrame
import os
import audd_recognition
import last_fm, itunes, musicbrainz, spotify, deezer, youtube, genius, serper
import concurrent.futures
import shazam, acoustid_recognition
import uvloop


def get_coverart(artist_name, song_name, platform, platform_name):
    is_downloaded = platform.download_coverart(artist_name, song_name)
    return is_downloaded, platform_name


def coverart(artist_name, song_name):
    streaming_platforms = [
        (itunes, "itunes"),
        (spotify, "spotify"),
        (genius, "genius"),
        (deezer, "deezer"),
        (musicbrainz, "musicbrainz"),
        (last_fm, "last.fm")
    ]
    with concurrent.futures.ThreadPoolExecutor() as executor:

        future_to_platform = [executor.submit(get_coverart, artist_name, song_name, platform, platform_name) for
                              (platform, platform_name) in streaming_platforms]

        for future in concurrent.futures.as_completed(future_to_platform):
            is_downloaded, platform_name = future.result()
            if is_downloaded == "Successfully downloaded":
                return 1
            else:
                pass


def fetch_metadata_from_platform(platform, artist, song_name):
    return platform.get_metadata(artist, song_name)


def get_metadata(artist=None, song_name=None):
    streaming_platforms = [itunes, spotify, genius, deezer, musicbrainz, last_fm]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_platform = [executor.submit(fetch_metadata_from_platform, platform, artist, song_name) for
                              platform in streaming_platforms]

        for future in concurrent.futures.as_completed(future_to_platform):
            album_artist, artist_name, track_name, album_name, genre, release_date = future.result()
            if artist_name != "":
                return album_artist, artist_name, track_name, album_name, genre, release_date

    return album_artist, artist_name, track_name, album_name, genre, release_date


def fetch_metadata_and_coverart(artist, song_name):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        metadata_future = executor.submit(get_metadata, artist, song_name)
        coverart_future = executor.submit(coverart, artist, song_name)

        metadata_result = metadata_future.result()
        for future in concurrent.futures.as_completed([metadata_future]):
            album_artist, artist_name, track_name, album_name, genre, release_date = future.result()
        coverart_result = coverart_future.result()
    return album_artist, artist_name, track_name, album_name, genre, release_date, coverart_result


def set_metadata(artist, song_name, song_dir, url):
    try:
        INVALID_FILENAME_CHARS = "/\\:*?\"<>|"
        album_artist, artist_name, track_name, album_name, genre, release_date, download_status = fetch_metadata_and_coverart(
            artist, song_name)
        if artist_name != "" and track_name != "":
            audiofile = eyed3.load(song_dir)

            if audiofile.tag is None:
                audiofile.initTag(version=eyed3.id3.ID3_V2_3)

            audiofile.tag.artist = artist_name
            audiofile.tag.album = album_name
            audiofile.tag.album_artist = album_artist
            audiofile.tag.title = track_name
            audiofile.tag.genre = genre
            audiofile.tag.year = release_date

            if download_status != 1:
                serper.download_artwork(artist, song_name)

            audiofile.tag.images.set(3, open(f"{artist}_{song_name}_cover_art.jpg", 'rb').read(), 'images/jpeg')

            audiofile.tag.save(version=eyed3.id3.ID3_V2_3)

            if song_dir != f"{album_artist}_{track_name}.mp3":
                change_dir = f"{album_artist}_{track_name}.mp3"
                for char in INVALID_FILENAME_CHARS:
                    change_dir = change_dir.replace(char, "_")
                if not os.path.exists(change_dir):
                    os.rename(song_dir, change_dir)
                song_dir = change_dir
            return song_dir

        else:
            musician, track = uvloop.run(shazam.get_metadata(song_dir))
            if artist in musician:
                shazam.recognize_song(song_dir)
                song_dir = f"{musician} - {track}.mp3"
                for char in INVALID_FILENAME_CHARS:
                    song_dir = song_dir.replace(char, "_")


            else:
                audiofile = eyed3.load(song_dir)
                if audiofile.tag is None:
                    audiofile.initTag(version=eyed3.id3.ID3_V2_3)

                audiofile.tag.artist = artist
                audiofile.tag.title = song_name
                if url != "":
                    is_downloaded = serper.download_artwork(artist, song_name)
                    if is_downloaded != 1:
                        youtube.download_thumbnail(url)

                else:
                    url = uvloop.run(youtube.search_youtube_videos(f"{song_name} by {artist}"))
                    is_downloaded = serper.download_artwork(artist, song_name)
                    if is_downloaded != 1:
                        youtube.download_thumbnail(url)

                audiofile.tag.images.set(3, open(f"{artist}_{song_name}_cover_art.jpg", 'rb').read(), 'images/jpeg')

                audiofile.tag.save(version=eyed3.id3.ID3_V2_3)
                if song_dir != f"{artist}_{song_name}.mp3":
                    change_dir = f"{artist}_{song_name}.mp3"
                    for char in INVALID_FILENAME_CHARS:
                        change_dir = change_dir.replace(char, "_")
                    if not os.path.exists(change_dir):
                        os.rename(song_dir, change_dir)
                    song_dir = change_dir
            return song_dir

    except FileExistsError:
        print("File already exists")
        return song_dir


def upload(song_dir):
    artist, song_name = acoustid_recognition.recognize_song(song_dir)
    if artist == "" and song_name == "":
        successful_download = shazam.recognize_song(song_dir)
        if successful_download:
            return artist, song_name
        else:
            artist, song_name = audd_recognition.recognize_song(song_dir)
            return artist, song_name
    else:
        return artist, song_name
