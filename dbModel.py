from flask_peewee.db import Database
from flask.ext.admin import Admin

from peewee import *
DATABASE = {
    'name': 'data/db.db',
    'engine': 'peewee.SqliteDatabase',
}


db = SqliteDatabase('data/db.db')

class Product(Model):
    link = CharField(unique=True)
    name = CharField()
    price = CharField()
    pic = CharField()
    posCount = IntegerField()
    negCount = IntegerField()
    neutCount = IntegerField()

    class Meta:
        database = db # this model uses the people database

class Comment(Model):
    productLink = ForeignKeyField(Product, related_name='links')
    comment = TextField(unique=True)  

    class Meta:
        database = db # this model uses the people database


Product.create_table()
Comment.create_table()
