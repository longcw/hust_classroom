# coding: utf-8

from app import app
from models import ClassRoom

from flask import render_template, request


@app.route('/')
def index():
    return 'test'

@app.route('/test')
def test():
    return 'hahahaha'