# -*- coding: utf-8 -*-
"""
Parse the title of a YouTube video to try and get artist & song name
"""
from __future__ import print_function, absolute_import
import argparse

try:
    from youtube_title_parse import plugins
    from youtube_title_parse.core import mapArtistTitle, mapTitle, get_song_artist_title
except ImportError:
    import plugins
    from core import mapArtistTitle, mapTitle, get_song_artist_title

    print("There's an error")


def get_artist_title(text, options={}):
    """
    Parse method
    """
    result = get_song_artist_title(
        text,
        options,
        {
            "before": [plugins.remove_file_extensions, plugins.clean_fluff],
            "split": [plugins.split_artist_title, plugins.split_text],
            "after": [
                mapArtistTitle(plugins.clean_artist, plugins.clean_title),
                mapArtistTitle(plugins.clean, plugins.clean),
                mapTitle(plugins.clean_common_fluff),
            ],
        },
    )
    if result:
        return result[0], result[1]
    else:
        return None, None


def process(args):
    options = {}
    if args.defaultArtist:
        options["defaultArtist"] = args.defaultArtist
    if args.defaultTitle:
        options["defaultTitle"] = args.defaultTitle
    result = get_artist_title(args.youtube_title, options)
    if result:
        print(result)
    else:
        print(args.youtube_title)
    return result


def main():
    pass


if __name__ == "__main__":
    main()

