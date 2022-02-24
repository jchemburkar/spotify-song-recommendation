""" handles raw data coming in from api """
from datetime import datetime
from marshmallow import Schema, fields, pre_dump, post_dump

class TrackSchema(Schema):
    """ handles a raw track node """
    artists = fields.Str()
    id = fields.Str()
    popularity = fields.Float()
    release_date = fields.Str(attribute="album.release_date")
    song_name = fields.Str(attribute="name")

    @pre_dump
    def predump_track(self, data, **kwargs):
        """ flatten out artists """
        artist_names = [artist["name"] for artist in data["artists"]]
        data["artists"] = ",".join(artist_names)
        return data
    
    @post_dump
    def postdump_track(self, data, **kwargs):
        """ handle dates """
        datetime_format = f"%Y{'-%m-%d' if '-' in data['release_date'] else ''}"
        data["release_date"] = datetime.strptime(data["release_date"], datetime_format)
        return data
