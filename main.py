from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from random import choice
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///copah.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# login_manager = LoginManager()
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


class News(db.Model):
    __tablename__ = "news"
    ID = db.Column(db.Integer, primary_key=True)
    # author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # author = relationship("User", back_populates="posts")
    Title = db.Column(db.String(250), nullable=False)
    Blurb = db.Column(db.String(250))
    Date = db.Column(db.String(250), nullable=False)
    News = db.Column(db.Text, nullable=False)
    AKA = db.Column(db.String(40), nullable=False)


class Members(db.Model):
    __tablename__ = "members"
    FirstName = db.Column(db.String(250))
    LastName = db.Column(db.String(250))
    AKA = db.Column(db.String(250), primary_key=True)
    Major = db.Column(db.String(250))
    Birthday = db.Column(db.String(250))
    Address = db.Column(db.String(250))
    Address2 = db.Column(db.String(250))
    City = db.Column(db.String(250))
    State = db.Column(db.String(250))
    Zip = db.Column(db.String(250))
    CellPhone = db.Column(db.String(250))
    HomePhone = db.Column(db.String(250))
    EMail = db.Column(db.String(250))
    Work = db.Column(db.String(250))
    WebSiteURL = db.Column(db.String(250))
    WebSiteName = db.Column(db.String(250))
    MemberName = db.Column(db.String(250))
    Password = db.Column(db.String(250))
    Luncheon2000 = db.Column(db.Integer())
    Friend = db.Column(db.Integer())
    Football = db.Column(db.Integer())
    Basketball = db.Column(db.Integer())
    Hockey = db.Column(db.Integer())
    Owner = db.Column(db.String(250))
    Baseball = db.Column(db.Integer())
    Guests = db.Column(db.Integer())
    CN = db.Column(db.String(250))


class Pictures(db.Model):
    __tablename__ = "pictures"
    ID = db.Column(db.Integer, primary_key=True)
    Event = db.Column(db.String(100), nullable=False)
    File = db.Column(db.String(100), nullable=False)
    Comment = db.Column(db.Text)
    Rating = db.Column(db.Integer(), nullable=False)
    Number = db.Column(db.Integer(), nullable=False)
    ETitle = db.Column(db.String(250), nullable=False)


db.create_all()


@app.route('/')
def home():
    news = News.query.order_by(News.ID.desc()).all()[:5]
    random_picture = choice(Pictures.query.all())
    photofilename = "graphics/" + random_picture.Event + "/" + random_picture.File
    print(photofilename)
    return render_template("index.html", news=news, photo=random_picture, photo_filename=photofilename)


@app.route('/members')
def members():
    members = Members.query.order_by(Members.AKA).all()
    return render_template("people.html", members=members)


@app.route('/member')
def show_member():
    return abort(404)


@app.route('/history')
def history():
    return render_template("history.html")


@app.route('/history2')
def history2():
    return render_template("history2.html")


@app.route('/history3')
def history3():
    return render_template("history3.html")


if __name__ == "__main__":
    app.run(host='127.0.0.33', port=5000, debug=True)
