""" overall file for generating recommendations """
import argparse
import pandas as pd
from typing import Set
from constants import FEATURES
from extract import (
    get_multiple_tracks,
    get_playlist_data,
    get_multiple_tracks,
    get_artists_similar_artists,
    get_artists_top_tracks,
    get_tracks_audio_features
)
from schema import TrackSchema
from sklearn.metrics.pairwise import cosine_similarity

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
    top_tracks = list(top_tracks)
    audio_features = pd.DataFrame(get_tracks_audio_features(top_tracks))
    metadata = pd.DataFrame([TrackSchema().dump(track) for track in get_multiple_tracks(top_tracks)])
    similar_track_df = pd.merge(metadata, audio_features, how="inner", on="id").reindex(metadata.index)
    return similar_track_df


#############
# Transform #
#############

def normalize_audio_features(audio_features: pd.DataFrame) -> pd.DataFrame:
    """ normalize columns of audio features """
    for col in ['loudness', 'tempo', 'popularity']:
        num = audio_features[col] - audio_features[col].min()
        denom = audio_features[col].max() - audio_features[col].min()
        audio_features[col] = num / denom
    return audio_features


def vectorize_dataframe(audio_features: pd.DataFrame) -> pd.Series:
    """ flatten list of audio features into one vector """
    return audio_features[FEATURES].mean(axis=0)


######################
# overall generation #
######################

def generate_playlist_recommendations(playlist_id: str) -> None:
    """ given the playlist id, pull in relevant data and generate recommendations """
    # extract data
    playlist_data = get_playlist_data(playlist_id)
    similar_artists_top_tracks = get_similar_artists_top_tracks(playlist_data)

    # normalize data
    playlist_data = normalize_audio_features(playlist_data)
    similar_artists_top_tracks = normalize_audio_features(similar_artists_top_tracks)

    # apply similarities
    playlist_vector = vectorize_dataframe(playlist_data)
    similar_artists_top_tracks["similarity"] = cosine_similarity(similar_artists_top_tracks[FEATURES], playlist_vector.values.reshape(1, -1))
    return similar_artists_top_tracks.sort_values(by="similarity", ascending=False)


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
    recommendations = generate_playlist_recommendations(args.playlist_id)
    recommendations.to_csv("recommendation_data.csv")
    for index, row in enumerate(recommendations[:10].T.to_dict().values(), start=1):
        print(f"{index}. {row['song_name']} by {row['artists']}, uri: {row['uri']}")

    print("")
    print("All data can be found in recommendation_data.csv in the root folder!")


if __name__ == "__main__":
    main()
