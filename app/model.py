#general
import numpy as np

#plotting (to be removed)
from matplotlib import pyplot as plt

#save
from keras.models import load_model
from keras.models import model_from_json
import json

# images
from PIL import Image

#keras
from keras.preprocessing import image

#flask
from flask import Blueprint

mymodel = Blueprint("modelling", __name__)


# classes for prediction
def blindpred(X_test, model_path):
    '''Prediction without inputing labels
    X_test = matrix of images
    model_path = model file name (w/ extension .h5)
    '''
    id_label = import_labels(model_path)
    print(id_label)
    try:
        model = load_model(model_path)
        model.summary()
        model.get_config()
    except IOError:
        print("Check model name (", model_path, ") or run the training first")
        return

    output = model.predict(X_test)
    Y_pred_cutoff = cutoffprediction(output)
    output_class = model.predict_classes(X_test)
    print("Raw output", output)
    label_class = [id_label[c] for c in output_class]
    print("Class", output_class, label_class)
    print("N with probability less than cutoff", \
    len([i for i in Y_pred_cutoff if i == -1]), "/", len(Y_pred_cutoff))
    #print output
    Y_pred = output.argmax(axis=-1)
    #fg = plt.figure("histo prediction")
    #plt.hist(Y_pred, bins=len(id_label.values()))
    #tick_marks = np.arange(len(id_label.values()))
    #plt.xticks(tick_marks, id_label.values(), rotation=30)
    #plt.xlabel("Predicted Classes")
    #plt.ylabel("N of events")

    #fg = plt.figure("histo prediction with minimum probability")
    #plt.hist(Y_pred_cutoff, bins=len(id_label.values()) + 1)
    #tick_marks = np.arange(len(id_label.values()) + 1)
    #plt.xticks(tick_marks, ['none'] + id_label.values(), rotation=30)
    #plt.xlabel("Predicted Classes")
    #plt.ylabel("N of events")
    #plt.show()
    return label_class, Y_pred_cutoff


def cutoffprediction(output, cutoff=0.8):
    '''output = result of prediction
    cutoff = check if any of the probabilities is larger than cutoff.
    if not the predicted class is -1
    '''
    predcutoff = []
    for ex in output:
        if any([clp for clp in ex if clp > cutoff]):
            predcutoff.append(-1)
        else:
            predcutoff.append(ex.argmax(axis=-1))
    return predcutoff


# Load test images
def populate_X_y(inputfiles, label=0, r_w=150, r_h=150):
    x = []
    y = []
    for fp in inputfiles:
        try:
            img1 = np.array(image.load_img(fp, target_size=(r_w, r_h)))
            #img2 = np.array(Image.open(fp).resize((150, 150)))
            x.append(img1)
            if label:
                y.append(label)
        except:
            print("Error while reading image")
            continue
    X = np.array(x)
    X = X.astype('float32')
    X /= 255.  # this is VERY IMPORTANT!
    Y = np.array(y)

    print(X.shape, Y.shape)
    return X, Y


# file uploads
def import_labels(model_path):
    '''Transform a dictionary of the form key = "label", value = int to
    key = int, value = "label"
    '''
    dic = json.loads(open(model_path.replace(".h5", ".json"), 'r').read())

    inv_dic = {v: k for k, v in dic.items()}
    return inv_dic


# main
def runprediction(inputfiles, model_path, rw=128, rh=128):
    X_test = []

    for p in inputfiles:
        X, _ = populate_X_y(p, r_w=rw, r_h=rh)
        if len(X_test) > 0:
            X_test = np.concatenate((X_test, X))
        else:
            X_test = X
    return blindpred(X_test, model_path)