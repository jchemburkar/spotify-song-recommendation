build:
	docker build -f Dockerfile -t spotify-recommender .

run:
	docker run -it --rm spotify-recommender:latest bash

run-live:
	docker run -it --rm -v ~/projects/spotify-song-recommendation:/usr/src spotify-recommender:latest bash