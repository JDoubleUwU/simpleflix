#run models first to create the database and tables
#then run data to insert test data into database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import util.util as util
import model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = util.dbpath()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def buildgenre():
    genre1 = model.Genre("horror")
    genre2 = model.Genre("adventure")
    genre3 = model.Genre("comedy")
    with app.app_context():
        db.session.add(genre1)
        db.session.add(genre2)
        db.session.add(genre3)
        db.session.commit()

def builduser():
    user1 = model.User("John", "Doe", "test@test", "test")
    user2 = model.User("Jane", "Ode", "test2@test2", "test2")
    with app.app_context():
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

def buildmovie():
    smovie1 = model.MovieShow("Scary Movie", 1, "A scary move", "10-31-2000", 80)
    smovie2 = model.MovieShow("Super Scary Movie", 1, "It's a really scary move", "11-31-2001", 83)
    smovie3 = model.MovieShow("Really Scary Movie", 1, "You will wet the bed", "12-31-2002", 86)

    amovie1 = model.MovieShow("Ring of Lords", 2, "It's like Lord of the Rings", "5-5-2000", 300)

    cmovie1 = model.MovieShow("Tropic Thunder", 3, "A dude playing a dude playing another dude", "6-10-2007", 80)
    cmovie2 = model.MovieShow("The Interview", 3, "A journalist duo stop a nuclear threat", "12-11-2014", 99)
    with app.app_context():
        db.session.add(smovie1)
        db.session.add(smovie2)
        db.session.add(smovie3)
        db.session.add(amovie1)
        db.session.add(cmovie1)
        db.session.add(cmovie2)
        db.session.commit()

def buildfavorite():
    favorite1 = model.Favorite(1, 4)
    favorite2 = model.Favorite(2, 2)
    favorite3 = model.Favorite(2, 3)
    with app.app_context():
        db.session.add(favorite1)
        db.session.add(favorite2)
        db.session.add(favorite3)
        db.session.commit()

def buildhistory():
    history1 = model.History(1, 1)
    with app.app_context():
        db.session.add(history1)
        db.session.commit()


##########################################
if __name__ == '__main__':
    with app.app_context():
        buildgenre()
        builduser()
        buildmovie()
        buildfavorite()
        buildhistory()
        print("done inserting data into DB")
