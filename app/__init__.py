import os
from flask import Flask
from .config import Config

currentDir = "{}/instance".format(os.path.realpath(__package__))

app = Flask(__name__, instance_relative_config = True, instance_path= currentDir)


app.config.from_object(Config)
app.config.from_pyfile('config.py')

from app import views