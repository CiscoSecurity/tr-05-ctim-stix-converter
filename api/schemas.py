from marshmallow import ValidationError, Schema, fields, EXCLUDE

from api.constants import (
    DEFAULT_SOURCE,
    DEFAULT_SOURCE_URI,
    DEFAULT_EXTERNAL_ID_PREFIX,
    DEFAULT_CONFIDENCE,
    DEFAULT_PRODUCER,
    DEFAULT_TITLE
)


def validate_string(value):
    if value == '':
        raise ValidationError('Field may not be blank.')


def validate_positive(value):
    if value <= 0:
        raise ValidationError('Field should contain positive integer.')


class CommonEntitySchema(Schema):
    title = fields.String(
        validate=validate_string,
        required=False,
        missing=DEFAULT_TITLE
    )
    short_description = fields.String(
        validate=validate_string,
        required=False
    )
    description = fields.String(
        validate=validate_string,
        required=False
    )
    confidence = fields.String(
        validate=validate_string,
        required=False,
        missing=DEFAULT_CONFIDENCE
    )
    severity = fields.String(
        validate=validate_string,
        required=False
    )

    class Meta:
        unknown = EXCLUDE


class IndicatorSchema(CommonEntitySchema):
    producer = fields.String(
        validate=validate_string,
        required=False,
        missing=DEFAULT_PRODUCER
    )


class SightingSchema(CommonEntitySchema):
    count = fields.Integer(
        validate=validate_positive,
        required=False,
        missing=1
    )
    internal = fields.Boolean(
        required=False,
        missing=False
    )
    sensor = fields.String(
        validate=validate_string,
        required=False
    )


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
    indicator = fields.Nested(
        IndicatorSchema,
        required=False,
        missing=IndicatorSchema().load({})
    )
    sighting = fields.Nested(
        SightingSchema,
        required=False,
        missing=SightingSchema().load({})
    )

    class Meta:
        unknown = EXCLUDE
