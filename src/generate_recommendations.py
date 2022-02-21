""" overall file for generating recommendations """
import argparse
from extract import get_playlist_data, get_artists_top_tracks, get_artists_similar_artists

SAMPLE_PLAYLIST = "3capEdrsV9FqJRYlLXrqsF"  # the commute!
SAMPLE_ALBUM = "1XGGeqLZxjOMdCJhmamIn8"  # FM, Vince Staples
SAMPLE_TRACK = "5p8jlDLpuWRiuuNDBPC9bY?si=f2fdbcbf077a4b58"  # Hadouken, Chief Keef
SAMPLE_ARTIST = "4ytkhMSAnrDP8XzRNlw9FS"  # Vince Gauraldi Trio


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
    print(get_artists_similar_artists(SAMPLE_ARTIST))
    # playlist_data = get_playlist_data(args.playlist_id)


if __name__ == "__main__":
    main()
