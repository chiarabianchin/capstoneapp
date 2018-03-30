#general
import os
import sys
import numpy as np
import io
import json
import requests
import shutil

from flask import Blueprint, render_template, flash, request

#forms
from .forms import PhotoForm
from werkzeug.utils import secure_filename

#modelling
from .model import runprediction

# images
from PIL import Image

#keras
from keras.preprocessing import image


myapp = Blueprint("app", __name__)


@myapp.route("/", methods=['GET','POST'])
def index():
    form = PhotoForm()

    if request.method == 'POST':
        print("Post")
        file_path = os.path.join('app', 'static', 'images')

        # photo camera
        try:
            fc = request.files['photoshot']
            filename = secure_filename(fc.filename)
            file_name = os.path.join(file_path, filename)
            fc.save(file_name)
            return render_template("index.html", form=form, filenames=filename)
        except:
            pass
        # image from link or file
        form = PhotoForm()
        if not form.validate():
            flash("Invalid form")
            return render_template("index.html", form=form, filenames=None)

        f = form.photo.data
        url = form.link.data
        print ("reading form")
        # image from web link
        if url is not "":
            resp = requests.get(url, stream=True)
            if "png" in url:
                ext = ".png"
            elif "jpg" in url or "JPEG" in url:
                ext = ".png"
            else:
                flash("This format is not supported (only jpg or png)")
            filename = "user_img" + ext
            if resp.status_code == 200:
                with open(os.path.join(file_path, filename), 'wb') as outfile:
                    shutil.copyfileobj(resp.raw, outfile)
        # image from file
        if f is not None:
            # save to file
            filename = secure_filename(f.filename)
            file_name = os.path.join(file_path, filename)
            f.save(file_name)

        return render_template("index.html", form=form, filenames=filename)
    else:
        print("Returning the form", form)
        return render_template("index.html", form=form, filenames=None)



@myapp.route("/info")
def info():
    with open(os.path.join('app', 'static',\
    'model_Y5pat_tr3110_4noneg_v1132_4noneg_steps_per_epoch_100_epochs_20_validation_steps_10.json'),\
    'r') as f:
        json_data = json.loads(f.read())
    with open(os.path.join('app', 'static',\
    'ingredient_map.json'),\
    'r') as f:
        json_dic = json.loads(f.read())
    return render_template("info.html", food=json_data, dic=json_dic)


@myapp.route('/upload', methods=['POST', 'GET'])
def upload():
    # retrieve the picture to be identified
    fl = request.args.get('picture')
    f = os.path.join('app', 'static', 'images', fl)
    ml = None
    ml = request.args.get('mealtype')
    cutoff = 0.8
    try:
        user_cutoff = request.args.get('cutoff')
        if user_cutoff:
            cutoff = user_cutoff
    except:
        pass
    # read the model and make the prediction
    model_file = os.path.join('app', 'static', \
    'model_Y5pat_tr3110_4noneg_v1132_4noneg_steps_per_epoch_100_epochs_20_validation_steps_10.h5')
    # note: one list for the base folder name, another list for the subdirectories
    # this is due to the structure e.g. training/tomato
    output_class, negative, prob = runprediction([[f]], model_file, cutoff)
    print("Negative in view", negative)
    if negative[0] == - 1:
        print("I couldn't recongnize")
        flash("I couldn't recongnize the ingredient or your ingredient is not in the known list")
        return render_template("result.html", filename=fl, probs=prob,
                               classes=output_class)
    print(type(output_class))
    print("REturning ", fl)

    # read the mapper of the ingredients for giallo zafferano
    with open(os.path.join('app','static','ingredient_map.json'), 'r') as mapingjs:
        json_ingredients = json.loads(mapingjs.read())

    return render_template('upload.html', filename=fl, output=output_class,
                           maping=json_ingredients, mltype=ml)
    #return render_template('index.html', form=form)


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