# spotify-song-recommendation
Spotify playlist recs are almost exclusively of artists currently in the playlist. Can we do better?

## how to run

For starters, you will need a spotify developer account! Directions can be found [here](https://developer.spotify.com/documentation/web-api/quick-start/). When you have a developer account, you will want to add it to the client in the [utils file](utils.py)

To build the image needed to run the environment, use:
``` make build ```

To run the image, use:
``` make run ```

Note: there is an option in the makefile for running against a live version of the code (`make run-live`). It relies on a relative path, so please update there if you wish to work with this code!

## background

### why

I have sometimes been frustrated when building a playlist with the available recommendations. Typically, they rely heavily on similar tracks from artists already on the playlist. They end up being very homogenous with the songs already present, and often do not offer me songs I have not considered previously. In an ideal world, recs would do one (or both) of the following:
1. provide accurate recommendations of songs I already know, so I do not have to find them
2. provide songs that I do not know, but may meet the vibe/cadence of the playlist

### what

To try to address the why, this project begins to build out what a solution could look like. Pulling in audio features of songs, we can use distance metrics (in this case, cosine similarity) to compare candidates to the average song of the playlist. Baked into this are a couple key assumptions that would be interesting places for future exploration:
- the vector representing the "average" song of the playlist correctly represents all the songs in the playlist; in reality, there may be a couple groups of songs in the playlist. Clustering and vectorizing those, and comparing candidates to each cluster, could be a more natural way to address the data.
- the set of candidate songs is complete. In reality, it is the top tracks of all of the "related" artists to spotify. In a productionalized version of this, I would try crawling and storing as many songs and artists as possible, epxanding the pool of candidates beyond this simple search.

## did it work?

I think so! A simple trial run of this script has provided songs both unkown, and known but expected. It has provided me with songs to add to my playlists. This is extremely valuable to me, as I tend to listen to the same playlists often, but they can become very stale if I don't continue adding new songs to them.

## next steps

I mentioned a few of them above, but for a quicker summary:
- expand set of candidate songs
- cluster playlist / create more than a single aggregate vector
- consider additional features (genres, eg)
- experiment with distance metrics
- surely, much more than I can come up with off the top of my head!