#__init__
from flask import Flask
from .views import myapp
from .forms import myforms

app = Flask(__name__)
app.config.from_object('config')
#db.init_app(app)

app.register_blueprint(myapp)
app.register_blueprint(myforms)