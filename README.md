# spotify-song-recommendation
Spotify playlist recs are almost exclusively of artists currently in the playlist. Can we do better?

## how to run

For starters, you will need a spotify developer account! Directions can be found [here](https://developer.spotify.com/documentation/web-api/quick-start/). When you have a developer account, you will want to add it to the client in the [utils file](utils.py)

To build the image needed to run the environment, use:
``` make build ```

To run the image, use:
``` make run ```

Note: there is an option in the makefile for running against a live version of the code (`make run-live`). It relies on a relative path, so please update there if you wish to work with this code!