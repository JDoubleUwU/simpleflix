#run models first to create the database and tables
#then run data to insert test data into database

import util.util as util
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = util.dbpath()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    hashed_password = db.Column(db.String(100))

    def __init__(self, firstname, lastname, email, password):
        self.firstName = firstname
        self.lastName = lastname
        self.email = email
        self.password = password
        self.hashed_password = util.hashpassword(password)

class MovieShow(db.Model):
    __tablename__ = 'movie_show'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    description = db.Column(db.String(1000))
    release_date = db.Column(db.String(100))
    duration = db.Column(db.Integer)

    def __init__(self, title, genre_id, description, release_date, duration):
        self.title = title
        self.genre_id = genre_id
        self.description = description
        self.release_date = release_date
        self.duration = duration

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column('id', db.Integer, primary_key=True)
    genre = db.Column(db.String(100))

    def __init__(self, genre):
        self.genre = genre


class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie_show.id'))

    def __init__(self, user_id, movie_id):
        self.user_id = user_id
        self.movie_id = movie_id

class History(db.Model):
    __tablename__ = 'history'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie_show.id'))

    def __init__(self, user_id, movie_id):
        self.user_id = user_id
        self.movie_id = movie_id


########################################
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("done creating database with models")