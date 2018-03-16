#general
import os

from flask import Blueprint, render_template, redirect, url_for, flash, request

#forms
from .forms import PhotoForm
from werkzeug.utils import secure_filename


myapp = Blueprint("app", __name__)


@myapp.route("/")
def index():
    form = PhotoForm()
    return render_template("index.html", form=form)


@myapp.route("/info")
def info():
    return render_template("info.html")


@myapp.route('/upload', methods=['POST'])
def upload():
    flash(request.form)
    #if form.validate_on_submit():
        #f = form.photo.data
        #print(f)
        #if f:
            #flash("something loaded")
        #if form.submit:
            #flash("submitted")
            #return render_template("upload.html", form=form)
        #else:
            #return redirect(url_for('error'))

    return render_template('upload.html', form=request.form)


@myapp.route("/run")
def run():
    #perform calculation here
    return render_template("result.html")


@myapp.route("/error")
def error():
    return render_template("error.html")




# 1) come stampare l'output
# 2) ottenere dalla richiesta il form
# 3) ottenere il dato dell'immagine "form.photo"-like
# 4) copiare l'immagine sul server, come?