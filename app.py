# coding: utf-8

import os
import ConfigParser

from flask import Flask

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(APP_ROOT, 'config.ini')

cf = ConfigParser.ConfigParser()
cf.read(CONFIG_FILE)

DEBUG = cf.getboolean('app', 'debug')

myapp = Flask(__name__)
myapp.config.from_object(__name__)

if cf.getboolean('app', 'use_mysql'):
    from peewee import MySQLDatabase
    mysql_cf = ConfigParser.ConfigParser()
    mysql_cf.read('server_config/mysql.ini')
    db = MySQLDatabase(mysql_cf.get('mysql', 'database'), threadlocals=True, host=mysql_cf.get('mysql', 'host'),
                       user=mysql_cf.get('mysql', 'user'), password=mysql_cf.get('mysql', 'password'))
else:
    from peewee import SqliteDatabase
    db_database = os.path.join(APP_ROOT, cf.get('sqlite', 'database'))
    db = SqliteDatabase(db_database)