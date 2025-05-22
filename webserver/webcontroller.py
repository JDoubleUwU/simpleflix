import util.util as util
import sql.model as model

from flask import Blueprint, render_template, redirect, request, session, Flask, flash, url_for
from flask_sqlalchemy import SQLAlchemy


# Define a Blueprint
webcontroller_bp = Blueprint('webcontroller ', __name__, template_folder='templates')
app = Flask(__name__)
app.secret_key = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = util.dbpath()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Add a view to the Blueprint
@webcontroller_bp.route('/')
def index():
    if 'email' in session:
        return render_template("main.html")
    else:
        return redirect('/login')


@webcontroller_bp.route('/main')
def main():
    print("rendering main page")
    if 'email' in session:
        with app.app_context():
            genres = db.session.query(model.Genre).all()
            userhistory = db.session.query(model.MovieShow).filter(model.History.user_id == session['userid'], model.History.movie_id == model.MovieShow.id).all()
            for show in userhistory:
                print(show.genre_id)
            catalog = db.session.query(model.MovieShow).all()
            for show in catalog:
                print(show.genre_id)
        return render_template("main.html", userhistory=userhistory, catalog=catalog, genres=genres)
    else:
        return redirect('/login')

@webcontroller_bp.route('/favorites')
def favorites():
    if 'email' in session:
        with app.app_context():
            userfavorites = db.session.query(model.MovieShow).filter(model.Favorite.user_id == session['userid'], model.Favorite.movie_id == model.MovieShow.id).all()
            for show in userfavorites:
                print(show.title)
        return render_template("favorites.html", userfavorites=userfavorites)
    else:
        return redirect('/login')


@webcontroller_bp.route('/login')
def login():
    return render_template("login.html")

@webcontroller_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@webcontroller_bp.route('/register')
def register():
    return render_template("register.html")

@webcontroller_bp.route('/submitregistration', methods=['GET', 'POST'])
def submitregistration():
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    email = request.form.get('email').lower()
    password = request.form.get('password')

    newUser = model.User(firstName, lastName, email, password)
    with app.app_context():
        query = db.session.query(model.User).filter(model.User.email == email).all()
        #user has been created
        if not query:
            print("nothing to see here")
            with app.app_context():
                db.session.add(newUser)
                db.session.commit()
            flash("Account has successfully been created", "success")
            return redirect('/login')

        for user in query:
            print(user.hashed_password)
        #user already exists
        flash("Email has already been registered", "error")
        return redirect('/register')

@webcontroller_bp.route('/submitlogin', methods=['GET', 'POST'])
def submitlogin():
    email = request.form.get('email').lower()
    password = request.form.get('password')
    print(email, password)
    with app.app_context():
        query = db.session.query(model.User).filter(model.User.email == email, model.User.password == password).all()
        if not query:
            flash("Bad username/password", "error")
            return redirect('/login')
        else:
            session['email'] = query[0].email
            session['firstname'] = query[0].firstName
            session['lastname'] = query[0].lastName
            session['userid'] = query[0].id

    return redirect('/main')

@webcontroller_bp.route('/movieshow/<movieshowid>', methods=['GET', 'POST'])
def movieshow(movieshowid):
    print(movieshowid)
    session['movieshowid'] = movieshowid
    with app.app_context():
        movieshow = db.session.query(model.MovieShow).filter(model.MovieShow.id == movieshowid).all()
        favored = db.session.query(model.Favorite).filter(model.Favorite.movie_id == movieshowid, session['userid'] == model.Favorite.user_id).all()

        if(favored):
            print("movie is favored")
        else:
            print("movie is not favored")

    return render_template('/movieshow.html', movieshowid=movieshowid, movieshow=movieshow, favored=favored)


@webcontroller_bp.route('/addfav')
def addfav():
    print("hi from addfav")
    with app.app_context():
        newfav = model.Favorite(session['userid'], session['movieshowid'])
        db.session.add(newfav)
        db.session.commit()
    return redirect('/main')

@webcontroller_bp.route('/removefav')
def removefav():
    print("hi from removefav")
    with app.app_context():
        fav = db.session.query(model.Favorite).filter(model.Favorite.movie_id == session['movieshowid'], model.Favorite.user_id == session['userid']).all()
        for f in fav:
            db.session.delete(f)
        db.session.commit()

    return redirect('/main')

@webcontroller_bp.route('/play')
def play():
    print("hi from play")
    with app.app_context():
        currshow = db.session.query(model.History).filter(model.User.id == session['userid']).first()
        db.session.delete(currshow)

        nextshow = model.History(session['userid'], session['movieshowid'])
        db.session.add(nextshow)
        db.session.commit()
    return redirect('/main')

@webcontroller_bp.route('/filtershow/<genreid>', methods=['GET', 'POST'])
def filtershow(genreid):
    print("hi from filtershow")
    print(genreid)
    with app.app_context():
        catalog = db.session.query(model.MovieShow).filter(model.MovieShow.genre_id == genreid).all()
    return render_template('filtershow.html', catalog=catalog)

@webcontroller_bp.route('/searchshow', methods=['GET', 'POST'])
def searchshow():
    searchstr = request.form.get('searchstr').lower()
    print(searchstr)
    with app.app_context():
        searchresults = db.session.query(model.MovieShow).filter(model.MovieShow.title.contains(searchstr)).all()
        for show in searchresults:
            print(show.title)
    return render_template("searchshow.html", searchresults=searchresults)