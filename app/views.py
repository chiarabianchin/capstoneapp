#general
import os

from flask import Blueprint, render_template, redirect, url_for

#forms
from .forms import PhotoForm
from werkzeug.utils import secure_filename


myapp = Blueprint("app", __name__)


@myapp.route("/")
def index():

    return render_template("index.html")


@myapp.route("/info")
def info():
    return render_template("info.html")


@myapp.route('/upload', methods=['GET', 'POST'])
def upload():
    form = PhotoForm()
    if form.validate_on_submit():
        f = form.photo.data
        print(f)
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            myapp.instance_path, 'photos', filename
        ))
        return redirect(url_for('error'))

    return render_template('upload.html', form=form)


@myapp.route("/run")
def run():
    #perform calculation here
    return render_template("result.html")


@myapp.route("/error")
def error():
    return "Error"