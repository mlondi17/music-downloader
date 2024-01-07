# Music-Downloader

Download songs complete with metadata, including cover art, song name, and artist information. You can achieve this by providing a YouTube URL, specifying the artist and song name, or sharing a song for which you want metadata added. Additionally, use music recognition to download unidentified songs.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Getting Started


### Prerequisites

Install docker. Details on how to install docker on your machine can be found on https://www.docker.com/get-started/ . Creat a [spotify](https://developer.spotify.com/),[last_fm](https://www.last.fm/api),[genius](https://docs.genius.com/),[serper](https://serper.dev/),[youtube](https://developers.google.com/youtube/v3) account for the api key .

### Installation 

After installation and setting up docker. First you have to build your docker image. Do this by running   "docker build -t music-downloader ."  on your terminal. Then you need to run your docker container by running the command  "docker run -it  music-downloader 
" on your terminal.

## License

MIT License

## Acknowledgments
The code for the music generation  can be found on https://github.com/MartinWeiss01/shazam-cli-py 

