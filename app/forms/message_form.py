from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class MessageForm(FlaskForm):
    content = TextAreaField('Message', validators=[DataRequired()], widget=TextArea())
    submit = SubmitField('Send')