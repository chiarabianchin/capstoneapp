from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from wtforms.fields import TextField

#flask
from flask import Blueprint, flash

myforms = Blueprint("forms", __name__)


class PhotoForm(FlaskForm):
    photo = FileField("Upload Image ",
            validators=[FileAllowed(['jpg', 'png'], 'Images only!')],
            description="Upload an image from your computer")
    link = TextField("Link Image", description="Copy&Paste a link")
    submit = SubmitField('Upload')

    def validate(self):

        if self.photo.data is None and self.link.data is "":
            flash("At least one of the fields must have a value")
            return False

        if self.link.data:
            if "http" not in self.link.data:
                flash("Check the link")
                return False
        return True

class Cutoff(FlaskForm):

    def __init__(self):
        super(Cutoff, self).__init__()
        cutoff = DecimalField("Probability Cutoff", description="If none of the prediction has a probability higher than cutoff, no prediction is made")
