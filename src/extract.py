""" file for extracting data from api """
from client import Client
from typing import List, Dict, Optional
import pandas as pd
from schema import TrackSchema
from utils import split_list_n_sized_chunks

CLIENT = Client()

################
# helper funcs #
################

def get_track(track_id: str) -> Dict:
    """ extract a given track from api """
    data = CLIENT.make_spotify_request(f"/tracks/{track_id}")
    return data


def get_multiple_tracks(track_ids: List[str]) -> Dict:
    """ extract  multiple tracks from api """
    chunks = split_list_n_sized_chunks(track_ids, 50)
    to_return = []
    for chunk in chunks:
        song_ids = ",".join(chunk)
        track_data = CLIENT.make_spotify_request(f"/tracks?ids={song_ids}")
        to_return.extend(track_data["tracks"])
    return to_return


def get_tracks_audio_features(track_ids: List[str]) -> List[Dict]:
    """ extract a given track from api """
    chunks = split_list_n_sized_chunks(track_ids, 100)
    to_return = []
    for chunk in chunks:
        song_ids = ",".join(chunk)
        audio_features = CLIENT.make_spotify_request(f"/audio-features?ids={song_ids}")
        to_return.extend(audio_features["audio_features"])
    return to_return


def get_album(album_id: str) -> Dict:
    """ extract a given album from api """
    data = CLIENT.make_spotify_request(f"/albums/{album_id}")
    return data


def get_playlist(playlist_id: str) -> Dict:
    """ extract a given album from api """
    data = CLIENT.make_spotify_request(f"/playlists/{playlist_id}")
    return data


def get_artists_top_tracks(artist_id: str) -> Dict:
    """ get top tracks for a given artist """
    data = CLIENT.make_spotify_request(f"/artists/{artist_id}/top-tracks?market=US")
    return data


def get_artists_similar_artists(artist_id: str) -> Dict:
    """ get similar artists for a given artist """
    data = CLIENT.make_spotify_request(f"/artists/{artist_id}/related-artists")
    return data


def get_spotify_recommendation_by_seed(seed_artists: List[str], seed_genres: List[str], seed_tracks: List[str], optional_args: Optional[Dict] = {}) -> Dict:
    """takes in up to 5 artists and/or up to 5 tracks as seeds, then returns their recommendation
    example args: seed_artists, seed_genres, seed_tracks, max_acousticness, etc.
    """
    if not seed_artists and not seed_genres and not seed_tracks:
        return None
    
    url = f"/recommendations?market=US"
    for key, data in [("seed_artists", seed_artists), ("seed_genres", seed_genres), ("seed_tracks", seed_tracks)]:
        if data:
            url += f"&{key}={','.join(data)}"

    for key, value in optional_args.items():
        url = f"{url}&{key}={value}"

    data = CLIENT.make_spotify_request(url)
    return [TrackSchema().dump(track) for track in data.get("tracks")]


###############
# model funcs #
###############

def get_playlist_data(playlist_id: str) -> pd.DataFrame:
    """ extract relevant audio features and metadata for a playlist """
    playlist = get_playlist(playlist_id)
    tracks = [track["track"] for track in playlist.get("tracks", {}).get("items", [])]
    track_metadata = pd.DataFrame(TrackSchema().dump(tracks, many=True))
    track_audio_data = pd.DataFrame(get_tracks_audio_features(track_metadata["id"].unique()))

    # merge metadata and audio features, return
    data = pd.merge(track_metadata, track_audio_data, how="inner", on="id").reindex(track_metadata.index)
    return data
