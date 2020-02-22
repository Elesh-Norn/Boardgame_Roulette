from marshmallow import Schema, fields

class SearchSchema(Schema):
    name = fields.Str()
    player_number = fields.Integer()
    genre = fields.Str()
    difficulty = fields.Str()
    time = fields.Integer()
