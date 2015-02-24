# coding: utf-8

import os
import ConfigParser

from flask import Flask
from peewee import MySQLDatabase

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(APP_ROOT, 'server_config/config.ini')
DEBUG = True

myapp = Flask(__name__)
myapp.config.from_object(__name__)

cf = ConfigParser.ConfigParser()
cf.read(CONFIG_FILE)

db_host = cf.get('mysql', 'host')
db_user = cf.get('mysql', 'user')
db_password = cf.get('mysql', 'password')
db_database = cf.get('mysql', 'database')

db = MySQLDatabase(db_database, threadlocals=True, host=db_host, user=db_user, password=db_password)