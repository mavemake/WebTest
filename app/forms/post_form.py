from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea

class PostForm(FlaskForm):
    title = StringField('Title', validators=[Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()], widget=TextArea())
    media = FileField('Upload Photo/Video')
    submit = SubmitField('Post')