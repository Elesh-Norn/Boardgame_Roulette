from marshmallow import Schema, fields, validate


def no_string_none(x):
    if x == "None":
        return False
    return True


class SearchSchema(Schema):
    name = fields.Str()
    player_number = fields.Integer()
    genre = fields.Str(validate=validate.Length(1, 10))
    difficulty = fields.Str(validate=no_string_none)
    time = fields.Integer()
