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


class ProcessForm(FlaskForm):
    content = TextAreaField('STIX Data', validators=[DataRequired()])
    translate = SubmitField('Translate')
    bundle = TextAreaField('CTIM Data', render_kw={'readonly': True})
    submit = SubmitField('Submit to Private Intel')
