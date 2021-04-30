from bundlebuilder.constants import CONFIDENCE_CHOICES, \
    SEVERITY_CHOICES
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, \
    SelectField, FormField, IntegerField, BooleanField
from wtforms.validators import DataRequired

from api.constants import DEFAULT_SOURCE, DEFAULT_SOURCE_URI, \
    DEFAULT_EXTERNAL_ID_PREFIX, DEFAULT_PRODUCER, DEFAULT_TITLE, \
    DEFAULT_CONFIDENCE, DEFAULT_INTERNAL, DEFAULT_COUNT


class AuthorizeForm(FlaskForm):
    client_id = StringField('CTR Client', validators=[DataRequired()])
    client_password = PasswordField(
        'CTR Password', validators=[DataRequired()]
    )
    region = SelectField('Region', choices=['us', 'eu', 'apjc'], default='us')
    submit = SubmitField('Authorize')


class CommonEntityForm(FlaskForm):
    title = StringField(
        'Title', validators=[DataRequired()], default=DEFAULT_TITLE
    )
    short_description = StringField('Short Description')
    confidence = SelectField(
        'Confidence', validators=[DataRequired()], choices=CONFIDENCE_CHOICES,
        default=DEFAULT_CONFIDENCE
    )
    severity = SelectField(
        'Severity', choices=[*SEVERITY_CHOICES, ''], default=''
    )


class IndicatorForm(CommonEntityForm):
    producer = StringField(
        'Producer', validators=[DataRequired()], default=DEFAULT_PRODUCER
    )


class SightingForm(CommonEntityForm):
    count = IntegerField(
        'Count', validators=[DataRequired()], default=DEFAULT_COUNT
    )
    internal = BooleanField(
        'Internal', default=DEFAULT_INTERNAL
    )


class ProcessForm(FlaskForm):
    content = TextAreaField('STIX Data', validators=[DataRequired()])

    exclude = StringField('Exclude')

    external_id_prefix = StringField(
        'External ID Prefix', validators=[DataRequired()],
        default=DEFAULT_EXTERNAL_ID_PREFIX
    )
    source = StringField(
        'Source',  validators=[DataRequired()], default=DEFAULT_SOURCE
    )
    source_uri = StringField(
        'Source URI', validators=[DataRequired()], default=DEFAULT_SOURCE_URI
    )

    indicator = FormField(IndicatorForm)
    sighting = FormField(SightingForm)

    translate = SubmitField('Convert')

    bundle = TextAreaField('CTIM Bundle', render_kw={'readonly': True})
    submit = SubmitField('Submit to Private Intelligence')
