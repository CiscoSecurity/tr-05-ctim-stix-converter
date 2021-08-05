from marshmallow import ValidationError, Schema, fields, EXCLUDE

from api.constants import (
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

    class Meta:
        unknown = EXCLUDE
