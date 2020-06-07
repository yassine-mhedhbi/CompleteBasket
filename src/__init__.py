from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf import CsrfProtect

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='DemoWhatevs')
Bootstrap(app)
CsrfProtect(app)

from src import basketapp