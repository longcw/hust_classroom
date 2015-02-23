# coding: utf-8

from app import myapp
from models import ClassRoom
from spider import ClassRoomSpider, Buildings

from flask import *
from peewee import DoesNotExist


@myapp.route('/')
def index():
    return redirect(url_for('classroom'))


@myapp.route('/classroom/')
@myapp.route('/classroom/<building>/')
@myapp.route('/classroom/<building>/<date>/')
def classroom(building='d9', date='0'):
    if building not in Buildings.keys():
        abort(404)
    date = int(date)
    date_str = ClassRoomSpider.get_date(date)
    try:
        classroom_obj = ClassRoom.get(date=date_str, building=building)
    except DoesNotExist:
        spider = ClassRoomSpider()
        classroom_obj = spider.get_and_save(date_str, building)

    title = u'%s教室-%s' % (building, date_str)
    current = {
        'building': building,
        'date': date
    }
    return render_template(
        'classroom.html',
        title=title,
        classroom=classroom_obj,
        buildings=Buildings,
        current=current
    )