from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

#flask
from flask import Blueprint

myforms = Blueprint("forms", __name__)


class PhotoForm(FlaskForm):
    photo = FileField("Upload Image ", validators=[FileRequired(),
                                  FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Upload')