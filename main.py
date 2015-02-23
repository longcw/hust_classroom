# coding :utf-8

from app import myapp, db
from models import ClassRoom
import view

db.create_tables([ClassRoom], safe=True)
if __name__ == '__main__':
    db.create_tables([ClassRoom], safe=True)
    myapp.run('0.0.0.0')
