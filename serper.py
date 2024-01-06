import requests
import json
from dotenv import load_dotenv
import os
import re
from logs import logger_func

logger = logger_func(__name__)
load_dotenv()

url_images = "https://google.serper.dev/images"


def download_artwork(artist, song_title):
    payload = json.dumps({
        "q": f"{artist} {song_title}"
    })
    headers = {
        'X-API-KEY': os.getenv("X_API_KEY"),
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", url_images, headers=headers, data=payload)
        if response.status_code == 200:
            data = response.json()
            if "images" in data:
                youtube_pattern = r'^https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w-]+'
                i = 0
                while i < len(data['images']):
                    link = data["images"][i]['link']
                    if not re.match(youtube_pattern, link):
                        coverart_url = data["images"][i]['imageUrl']
                        coverart_response = requests.get(coverart_url)

                        with open(f"{artist}_{song_title}_cover_art.jpg", 'wb') as f:
                            f.write(coverart_response.content)
                        logger.info(f"Downloaded artwork for {artist} by {song_title}")
                        return 1
                    else:
                        i += 1

            else:
                logger.info(f"Cannot find images of {artist}-{song_title} ")
        else:
            logger.info(f"Failed to fetch data for {artist} by {song_title} ")
    except Exception as e:
        logger.info(f"An error occurred: {e}")


