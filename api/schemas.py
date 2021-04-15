from marshmallow import ValidationError, Schema, fields, INCLUDE, pre_load

from api.constants import (
    DEFAULT_SOURCE,
    DEFAULT_SOURCE_URI,
    DEFAULT_EXTERNAL_ID_PREFIX,
    NON_CUSTOMIZABLE_FIELDS
)


def validate_string(value):
    if value == '':
        raise ValidationError('Field may not be blank.')


class ArgumentsSchema(Schema):
    content = fields.String(
        validate=validate_string,
        required=True
    )
    exclude = fields.List(
        fields.String(validate=validate_string),
        required=False,
        missing=[]
    )
    source = fields.String(
        validate=validate_string,
        required=False,
        missing=DEFAULT_SOURCE
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

    @pre_load
    def check_forbidden_fields(self, data, **kwargs):
        data = {} if data is None else data
        if set(NON_CUSTOMIZABLE_FIELDS).intersection(data.keys()):
            raise ValidationError(
                f'Fields: {", ".join(NON_CUSTOMIZABLE_FIELDS)}'
                ' are not allowed to customize.'
            )
        return data

    class Meta:
        unknown = INCLUDE
