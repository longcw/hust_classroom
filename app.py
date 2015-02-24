# coding: utf-8

import os

from flask import Flask
from peewee import SqliteDatabase, MySQLDatabase

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
# DATABASE = os.path.join(APP_ROOT, 'classroom.db')
DEBUG = True

myapp = Flask(__name__)
myapp.config.from_object(__name__)
# db = SqliteDatabase(myapp.config['DATABASE'], threadlocals=True)
db = MySQLDatabase('hust.longc.wang', threadlocals=True, host='localhost', user='root', password='123456')