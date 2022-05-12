from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


class CreateNewsPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    blurb = StringField("Blurb", validators=[DataRequired()])
    news = CKEditorField("News", validators=[DataRequired()])
    submit = SubmitField("Submit")
