""" overall file for generating recommendations """
import argparse
import pandas as pd
from typing import Set
from extract import (
    get_playlist_data,
    get_multiple_tracks,
    get_artists_similar_artists,
    get_artists_top_tracks,
    get_tracks_audio_features
)

SAMPLE_PLAYLIST = "3capEdrsV9FqJRYlLXrqsF"  # the commute!
SAMPLE_ALBUM = "1XGGeqLZxjOMdCJhmamIn8"  # FM, Vince Staples
SAMPLE_TRACK = "5p8jlDLpuWRiuuNDBPC9bY"  # Hadouken, Chief Keef
SAMPLE_ARTIST = "4ytkhMSAnrDP8XzRNlw9FS"  # Vince Gauraldi Trio

###########
# extract #
###########

def _get_playlist_similar_artists(playlist_data: pd.DataFrame) -> Set[str]:
    """ get the set of artist_ids of all artists in or related to a playlist """
    print("Finding all artists related to given playlist")
    track_data = get_multiple_tracks(playlist_data["id"])
    artist_set = set()
    for track in track_data:
        for artist in track["artists"]:
            if artist["id"] not in artist_set:
                similar_artists = get_artists_similar_artists(artist["id"])
                for similar_artist in similar_artists["artists"]:
                    artist_set.add(similar_artist["id"])
            artist_set.add(artist["id"])
    
    print(f"Found {len(artist_set)} artist ids")
    return artist_set


def get_similar_artists_top_tracks(playlist_data: pd.DataFrame) -> pd.DataFrame:
    """ given playlist data, pull list of all related artists; grab their top tracks, and filter out those present in playlist """
    similar_artists = _get_playlist_similar_artists(playlist_data)
    print("Getting top tracks for artists")
    top_tracks = set()
    for artist_id in similar_artists:
        artists_top_tracks = get_artists_top_tracks(artist_id)
        for track in artists_top_tracks["tracks"]:
            top_tracks.add(track["id"])

    print(f"Found {len(top_tracks)} tracks")
    audio_features = get_tracks_audio_features(list(top_tracks))
    return audio_features


######################
# overall generation #
######################

def generate_playlist_recommendations(playlist_id: str) -> None:
    """ given the playlist id, pull in relevant data and generate recommendations """
    playlist_data = get_playlist_data(playlist_id)
    get_similar_artists_top_tracks(playlist_data)


########
# main #
########

def get_args() -> argparse.Namespace:
    """ gets arguments from command line """
    parser = argparse.ArgumentParser()
    parser.add_argument("--playlist_id", required=True, type=str)
    return parser.parse_args()


def main():
    """ main func """
    args = get_args()
    generate_playlist_recommendations(args.playlist_id)


if __name__ == "__main__":
    main()
