#general
import os
import sys
import numpy as np
import io

from flask import Blueprint, render_template, redirect, url_for, flash, request

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
    ingredients = []
    try:
        print("Request ", request.args.get('filenames'))
        ingredients = request.args.get('filenames')
    except:
        print("Ingredients not yet created")
        ingredients = []
        pass
    if ingredients is None:
        ingredients = []
    print("ingredients", ingredients)
    if request.method == 'POST':
        print("I'm validate on submit")
        form = PhotoForm()
        f = form.photo.data
        # save to file
        filename = secure_filename(f.filename)
        file_name = os.path.join('app','static', 'images', filename)
        print("Saving file to ", file_name)
        f.save(file_name)
        print("Done")
        print("array", np.array(form.photo))
        ingredients.append(filename)
        print("Now ingredients", ingredients)
        return render_template("index.html", form=form, filenames=ingredients)
    else:
        print("Returning the form", form)
        return render_template("index.html", form=form, filenames=ingredients)



@myapp.route("/info")
def info():
    return render_template("info.html")


@myapp.route('/upload')
def upload():
    print ("test")
    fl = request.args.get('picture')
    print(fl)
    f = os.path.join('app', 'static', 'images', fl)

    #for fp in [[f]]:
        #for test in fp:
            #img1 = np.array(image.load_img(test, target_size=(150, 150)))
            #print("Img ", img1)
    model_file = os.path.join('app', 'static', \
    'model_Y5pat_tr3110_4noneg_v1132_4noneg_steps_per_epoch_100_epochs_20_validation_steps_10.h5')
    # note: one list for the base folder name, another list for the subdirectories
    # this is due to the structure e.g. training/tomato
    output_class = runprediction([[f]], model_file)
    print(type(output_class))
    print(type(output_class[0]), type(output_class[1]))
    print("REturning ", fl)
    return render_template('upload.html', filename=fl, output=output_class)
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