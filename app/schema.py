from marshmallow import Schema, fields, validate



class SearchSchema(Schema):
    name = fields.Str()
    player_number = fields.Integer()
    genre = fields.Str(validate=validate.Length(1, 10))
    difficulty = fields.Str()
    time = fields.Integer()
