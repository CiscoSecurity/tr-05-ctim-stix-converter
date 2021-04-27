from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, \
    SelectField
from wtforms.validators import DataRequired


class AuthorizeForm(FlaskForm):
    client_id = StringField('CTR Client', validators=[DataRequired()])
    client_password = PasswordField(
        'CTR Password', validators=[DataRequired()]
    )
    region = SelectField('Region', choices=['us', 'eu', 'apjc'], default='us')
    submit = SubmitField('Authorize')


class TranslateForm(FlaskForm):
    content = TextAreaField('STIX Data', validators=[DataRequired()])
    submit = SubmitField('Translate')


class SubmitForm(FlaskForm):
    bundle = TextAreaField('CTIM Data', validators=[DataRequired()], render_kw={'readonly': True})
    submit = SubmitField('Submit to Private Intel')
