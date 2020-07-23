import os
from sqlalchemy import Table, Column, String, Integer, create_engine, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import Date, Enum
from sqlalchemy.orm import relationship

import json

# set database path from environment, else set default
try:
    database_path = os.environ.get('DATABASE_URL') 
except:
    database_name = "agency"
    database_path = "postgresql:///{}".format(database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    if app.config['TESTING']:
        db.session.commit()
        db.drop_all()
        db.create_all() # not necessary in production - we use migrations


'''
Movie

'''

class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    releasedate = Column(Date)
    actors = relationship('Actor', secondary = 'link')

    def __init__(self, title, releasedate):
        self.title = title
        self.releasedate = releasedate

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'releasedate': self.releasedate
        }


'''
Actors

'''

class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(Enum("female", "male", "unspecified", name="gender_enum", create_type=False))
    movies = relationship('Movie', secondary = 'link')

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

class Link(db.Model):
   __tablename__ = 'link'
   actor_id = Column(
       Integer, 
       ForeignKey('actors.id'), 
       primary_key = True)

   movie_id = Column(
       Integer, 
       ForeignKey('movies.id'), 
       primary_key = True)