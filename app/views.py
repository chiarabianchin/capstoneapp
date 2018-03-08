from flask import Blueprint, render_template

myapp = Blueprint("app", __name__)


@myapp.route("/")
def index():

    return render_template("index.html")