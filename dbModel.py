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

class Vibe(Model):
    productLink = ForeignKeyField(Product, related_name='vibes')
    
    posCount = IntegerField()
    negCount = IntegerField()
    neutCount = IntegerField()
    subjectivity = FloatField()

    #avgLegnth = IntegerField()
    class Meta:
        database = db # this model uses the people database

class Sentence(Model):
    productLink = ForeignKeyField(Product, related_name='products') 
    comment = ForeignKeyField(Comment, related_name='fromComment') 
    vibe = FloatField() 
    subjectivity = FloatField()
    length = IntegerField()
    #avgLegnth = IntegerField()
    class Meta:
        database = db # this model uses the people database


Product.create_table() 
Comment.create_table() 
Vibe.create_table() 
Sentence.create_table() 
