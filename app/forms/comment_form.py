from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()], widget=TextArea())
    media = FileField('Upload Photo/Video')
    submit = SubmitField('Comment')