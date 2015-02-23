# coding: utf-8

import os

from flask import Flask
from peewee import SqliteDatabase

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(APP_ROOT, 'classroom.db')
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
db = SqliteDatabase(app.config['DATABASE'], threadlocals=True)