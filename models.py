# coding: utf-8

import datetime

from peewee import *
from application import db


class BaseModel(Model):
    class Meta:
        database = db


class ClassRoom(BaseModel):
    date = CharField()
    building = CharField()
    data = TextField()
    update_time = DateTimeField(default=datetime.datetime.now())

    @staticmethod
    def save_data(date, building, data):
        try:
            item = ClassRoom.get(date=date, building=building)
        except DoesNotExist:
            item = ClassRoom()
        item.building = building
        item.date = date
        item.data = data
        item.update_time = datetime.datetime.now()
        item.save()
        return item