from marshmallow import ValidationError, Schema, fields

from api.constants import (
    DEFAULT_SOURCE,
    DEFAULT_SOURCE_URI,
    DEFAULT_EXTERNAL_ID_PREFIX
)


def validate_string(value):
    if value == '':
        raise ValidationError('Field may not be blank.')


class ArgumentsSchema(Schema):
    file = fields.String(
        validate=validate_string,
        required=True
    )
    source = fields.String(
        missing=DEFAULT_SOURCE,
        validate=validate_string,
        required=False
    )
    source_uri = fields.String(
        validate=validate_string,
        required=False,
        missing=DEFAULT_SOURCE_URI
    )
    external_id_prefix = fields.String(
        validate=validate_string,
        required=False,
        missing=DEFAULT_EXTERNAL_ID_PREFIX
    )
    exclude = fields.List(
        fields.String(
            validate=validate_string
        ),
        required=False,
        missing=[]
    )
