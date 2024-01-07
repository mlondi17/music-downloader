# Music Downloader

Effortlessly download songs with complete metadata, encompassing cover art, song name, and artist information. This tool empowers users to acquire music from diverse sources, offering the flexibility of inputting a YouTube URL, specifying the artist and song name, or providing a song for which metadata needs augmentation. Additionally, leverage music recognition to download unidentified songs seamlessly.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Getting Started

### Prerequisites

Ensure Docker is installed on your machine. If not, refer to the [official Docker installation guide](https://www.docker.com/get-started/). Create accounts for the following services to obtain the required API keys:

- [Spotify Developer](https://developer.spotify.com/)
- [Last.fm API](https://www.last.fm/api)
- [Genius](https://docs.genius.com/)
- [Serper](https://serper.dev/)
- [YouTube API](https://developers.google.com/youtube/v3)

### Installation 

After installing Docker and acquiring the necessary API keys:

1. Build your Docker image using the following command in your terminal:
   ```bash
   docker build -t music-downloader .
   ```
  Then you need to run your docker container by running the command  
  ```bash
  docker run -it  music-downloader 
  ```

## License

This project is licensed under the [MIT License]()

## Acknowledgments
The code for the music generation  can be found [here](https://github.com/MartinWeiss01/shazam-cli-py) 

