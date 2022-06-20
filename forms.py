from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, FileField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class CreateNewsPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    blurb = StringField("Blurb", validators=[DataRequired()])
    news = CKEditorField("News", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CreateEventForm(FlaskForm, list):
    name = StringField("Name", validators=[DataRequired()])
    type = SelectField("Type", choices=[('T', '45 Tournament'), ('K', 'Karaoke'), ('P', 'Parties'), ('O', 'Other')])
    date = StringField("Date")
    location = StringField("Location")
    picture_key = SelectField("Picture Gallery", choices=list)
    thumbnail = StringField("Thumbnail")
    body = CKEditorField("Body")
    submit = SubmitField("Submit")


class FflSeasonUploadForm(FlaskForm):
    year = SelectField("Year", choices=list)
    file = FileField("Season File")
    submit = SubmitField("Submit")
