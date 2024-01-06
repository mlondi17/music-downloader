import metadata
import youtube
import shazam, acoustid_recognition, audd_recognition
import uvloop


def main():
    print("1.Download using youtube url\n2.Download song by using artist name & song name\n3.Upload song as a "
          "mp3\n4.Send recording of song\n")
    user_options = int(input("Option:"))

    if user_options == 1:
        url = input("Youtube url:")
        print("Processing url...")
        artist, song_name = youtube.get_metadata(url)
        if artist is not None:
            song_dir, video_url = uvloop.run(youtube.download_video(artist, song_name, url))
            metadata.set_metadata(artist, song_name, song_dir, video_url)
            print("Done")
        else:
            print('Try a different option as artist name & song name cannot be extracted')

    elif user_options == 2:
        artist_name = input("Artist name:")
        song_name = input("Song name:")
        song_dir, video_url = uvloop.run(youtube.download_video(artist_name, song_name))
        if video_url != "":
            print("Processing metadata...")
            artist, song_name = youtube.get_metadata(
                video_url)  # for cases where the user doesn't enter the required artist
            metadata.set_metadata(artist, song_name, song_dir, video_url)
            print("Done")
        else:
            print("Couldn't find music to download")

    elif user_options == 3:
        song_dir = input("Song path:")
        url = ""
        print("Finding song...")
        artist_name, song_name = metadata.upload(song_dir)
        if artist_name != "" and song_name != "":
            print("Processing metadata...")
            metadata.set_metadata(artist_name, song_name, song_dir, url)
            print("Done")
        else:
            print("Sorry,Couldn't find artist and song name")

    elif user_options == 4:
        url = ""
        track_dir = input("Voice recording path:")
        print("Finding song...")
        artist_name, track_name = acoustid_recognition.recognize_song(
            track_dir)
        if artist_name == "" and track_name == "":
            artist_name, track_name = uvloop.run(shazam.get_metadata(track_dir))
            if artist_name != "" and track_name != "":
                song_dir, video_url = uvloop.run(youtube.download_video(artist_name, track_name, url))
                shazam.recognize_song(song_dir)

            else:
                artist_name, track_name = audd_recognition.recognize_song(track_dir)
                if artist_name != "" and track_name != "":
                    song_dir, video_url = uvloop.run(youtube.download_video(artist_name, track_name))
                    print("Processing metadata...")
                    metadata.set_metadata(artist_name, track_name, song_dir, video_url)
                    print("Done")
                else:
                    print("Sorry, song cannot be found")

        else:
            song_dir, video_url = uvloop.run(youtube.download_video(artist_name, track_name))
            print("Processing metadata...")
            metadata.set_metadata(artist_name, track_name, song_dir, video_url)


if __name__ == "__main__":
    main()
