import yt_dlp
import requests
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from unidecode import unidecode
import spotify
import time
import concurrent.futures
from parse import get_artist_title
from logs import logger_func

logger = logger_func(__name__)

st = time.time()
load_dotenv()

api_key = os.getenv("YOUTUBE_API_KEY")


async def download_video(artist=None, song_name=None, urls=None):
    try:
        video_url = ""
        ydl_opts = {
            'default_search': 'ytsearch',
            'quiet': True,
            'format': 'bestaudio/best',
            'outtmpl': f'{artist}_{song_name}.%(ext)s',
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', },
                {'key': 'FFmpegMetadata', 'add_metadata': True}
            ]
        }
        with concurrent.futures.ThreadPoolExecutor() as executor:
            if artist != "" and (urls == "" or urls is None):
                query = f"{song_name} by {artist}"
                f1 = executor.submit(search_youtube_videos, query)
                video_url = f1.result()
                urls = video_url
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if urls is not None:
                error_code = ydl.download(urls)
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    f2 = executor.submit(get_metadata, urls)
                    artist_name, track_name = f2.result()
                song_dir = f'{artist_name}_{track_name}.mp3'
                if song_dir != f"{artist}_{song_name}.mp3":
                    os.rename(f'{artist}_{song_name}.mp3', song_dir)
                return song_dir, urls

            else:
                download_status = spotify.download_song(artist, song_name)
                if not download_status:
                    query = f'{artist} {song_name}'  # Create a search query
                    info = ydl.extract_info(query, download=True)
                    if 'entries' in info:
                        # Find the first video in the search results
                        video = info['entries'][0]
                        # Download the video
                        ydl.download([video['url']])
                        song_dir = f'{artist}_{song_name}.mp3'
                        return song_dir, urls

                    else:
                        logger.info(f"No video found for '{song_name}' by {artist}")
                        return None
                else:
                    song_dir = f'{artist}_{song_name}.mp3'
                    video_url = ""
                    return song_dir, video_url
    except OSError as e:
        logger.info(f"An error occurred while renaming the file: {e}")

    except Exception as e:
        logger.info(f"An error occurred: {e}")


def download_thumbnail(video_url):
    try:
        request_url = f"https://www.youtube.com/oembed?url={video_url}&format=json"

        response = requests.get(request_url)
        response.raise_for_status()

        song_metadata = response.json()
        if song_metadata:
            artwork_url = song_metadata['thumbnail_url']
            response = requests.get(artwork_url)
            artist, song_title = get_metadata(video_url)
            if response.status_code == 200:
                with open(f"{artist}_{song_title}_cover_art.jpg", 'wb') as f:
                    f.write(response.content)
                logger.info(f"Successfully downloaded thumbnail for {artist}-{song_title}")
                return "Successfully downloaded"
            else:
                logger.info(f"Failed to download artwork for {artist} by {song_title} on itunes")
        else:
            logger.info("Link for song not found on youtube.")

    except requests.exceptions.HTTPError as e:
        logger.info(f"HTTP error occurred: {e}")

    except requests.exceptions.RequestException as e:
        logger.info(f"Request error occurred: {e}")
    except Exception as e:
        logger.info(f"An unexpected error occurred: {e}")


def get_metadata(video_url):
    try:
        request_url = f"https://www.youtube.com/oembed?url={video_url}&format=json"

        response = requests.get(request_url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        song_metadata = response.json()
        if song_metadata:
            if " - " in song_metadata['author_name']:  # e.g artist_name - Topic
                artist_name = song_metadata['author_name'].split("-")
                artist = artist_name[0].strip()
                song_name = song_metadata['title']

                # removing invalid characters
                invalid_chars = r'\/:*?"<>|'

                artist = ''.join(char if char not in invalid_chars else '' for char in artist)
                song_name = ''.join(char if char not in invalid_chars else '' for char in song_name)
                return artist, song_name
            else:
                title = unidecode(song_metadata['title'])
                artist, song_name = get_artist_title(title)
                return artist, song_name


        else:
            logger.info(f"Link {video_url} for song not found on youtube.")

    except requests.exceptions.HTTPError as e:
        logger.info(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        logger.info(f"Request error occurred: {e}")
    except Exception as e:
        logger.info(f"An unexpected error occurred: {e}")


async def search_youtube_videos(query):
    youtube = build("youtube", "v3", developerKey=api_key)

    search_response = youtube.search().list(
        q=query,
        type="video",
        part="id",
        maxResults=1
    ).execute()
    if "items" in search_response and search_response["pageInfo"]['totalResults'] > 1:
        video_id = search_response["items"][0]["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url
    else:
        return None




