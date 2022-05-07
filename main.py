from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from random import choice
import os
import requests

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
    State = db.Column(db.String(2))
    Zip = db.Column(db.String(10))
    CellPhone = db.Column(db.String(250))
    HomePhone = db.Column(db.String(250))
    EMail = db.Column(db.String(250))
    Work = db.Column(db.String(250))
    WebSiteURL = db.Column(db.String(250))
    WebSiteName = db.Column(db.String(250))
    MemberName = db.Column(db.String(250))
    Password = db.Column(db.String(250))
    Picture = db.Column(db.String(250))
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


class Rank(db.Model):
    __tablename__ = "ranks"
    AKA = db.Column(db.String(250), primary_key=True)
    Tourney2 = db.Column(db.Integer)
    Tourney3 = db.Column(db.Integer)
    Tourney4 = db.Column(db.Integer)
    Active = db.Column(db.Integer)
    Tourney1 = db.Column(db.Integer)
    T1P = db.Column(db.Integer)
    T1F = db.Column(db.Integer)
    T1C = db.Column(db.Integer)
    T2P = db.Column(db.Integer)
    T2F = db.Column(db.Integer)
    T2C = db.Column(db.Integer)
    T3P = db.Column(db.Integer)
    T3F = db.Column(db.Integer)
    T3C = db.Column(db.Integer)
    T4P = db.Column(db.Integer)
    T4F = db.Column(db.Integer)
    T4C = db.Column(db.Integer)
    Current = db.Column(db.Integer)
    Tourney5 = db.Column(db.Integer)
    T5P = db.Column(db.Integer)
    T5F = db.Column(db.Integer)
    T5C = db.Column(db.Integer)
    RWin = db.Column(db.Integer)
    RLoss = db.Column(db.Integer)
    PWin = db.Column(db.Integer)
    PLoss = db.Column(db.Integer)
    FWin = db.Column(db.Integer)
    FLoss = db.Column(db.Integer)
    SixWin = db.Column(db.Integer)
    SixLoss = db.Column(db.Integer)
    Tourney6 = db.Column(db.Integer)
    T6P = db.Column(db.Integer)
    T6F = db.Column(db.Integer)
    T6C = db.Column(db.Integer)
    Tourney = db.Column(db.Integer)
    T7P = db.Column(db.Integer)
    T7F = db.Column(db.Integer)
    T7C = db.Column(db.Integer)
    Tourney8 = db.Column(db.Integer)
    T8P = db.Column(db.Integer)
    T8F = db.Column(db.Integer)
    T8C = db.Column(db.Integer)
    Tourney9 = db.Column(db.Integer)
    T9P = db.Column(db.Integer)
    T9F = db.Column(db.Integer)
    T9C = db.Column(db.Integer)


db.create_all()


@app.route('/')
def home():
    news = News.query.order_by(News.ID.desc()).all()[:5]
    random_picture = choice(Pictures.query.all())
    photofilename = "graphics/" + random_picture.Event + "/" + random_picture.File
    # print(photofilename)
    return render_template("index.html", news=news, photo=random_picture, photo_filename=photofilename)


@app.route('/members')
def members():
    members = Members.query.order_by(Members.AKA).all()
    return render_template("people.html", members=members)


@app.route('/member/<AKA>')
def show_member(AKA):
    member = Members.query.get(AKA)
    print(member)
    return render_template("member_profile.html", member=member)


@app.route('/history')
def history():
    return render_template("history.html")


@app.route('/history2')
def history2():
    return render_template("history2.html")


@app.route('/history3')
def history3():
    return render_template("history3.html")


@app.route('/archives')
def archives():
    news = News.query.order_by(News.ID.desc()).all()
    return render_template("index.html", news=news)


@app.route('/gallery')
def gallery():
    return render_template("gallery.html")


@app.route('/tournaments')
def tournaments():
    return render_template("tournaments.html")


@app.route('/tournament/<int:tourney_id>')
def tournament_detail(tourney_id):
    num = str(tourney_id)
    page = "tourney" + num + ".html"
    return render_template(page)


@app.route('/rankings')
def rankings():
    return render_template("rankings.html")


@app.route('/rank/1')
def rank_1():
    rows = Rank.query.order_by(Rank.Tourney1.desc()).all()
    list = [{"AKA": row.AKA,
             "Pts": row.Tourney1 + 1600,
             "Apps": 1,
             "TP": row.T1P,
             "TF": row.T1F,
             "TC": row.T1C} for row in rows if row.Tourney1 != 0 or row.AKA == "Jay-Ave" or row.AKA == "Serpentor"]
    return render_template("rank1.html", rows=list)


@app.route('/rank/2')
def rank_2():
    rows = Rank.query.order_by(Rank.Tourney2.desc()).all()
    list = [{"AKA": row.AKA,
             "Pts": row.Tourney2 + row.Tourney1 + 1600,
             "Apps": 2,
             "TP": row.T2P + row.T1P,
             "TF": row.T2F + row.T2F,
             "TC": row.T2C + row.T2C} for row in rows if row.Tourney2 != 0]
    return render_template("rank1.html", rows=list)


@app.route('/rank/3')
def rank_3():
    rows = Rank.query.order_by(Rank.Tourney3.desc()).all()
    list = [{"AKA": row.AKA,
             "Pts": row.Tourney3 + row.Tourney2 + row.Tourney1 + 1600,
             "Apps": 3,
             "TP": row.T3P + row.T2P + row.T1P,
             "TF": row.T3F + row.T2F + row.T1F,
             "TC": row.T3C + row.T2C + row.T1C} for row in rows if row.Tourney3 != 0]
    return render_template("rank1.html", rows=list)


@app.route('/rank/4')
def rank_4():
    rows = Rank.query.order_by(Rank.Tourney4.desc()).all()
    list = [{"AKA": row.AKA,
             "Pts": row.Tourney4 + row.Tourney3 + row.Tourney2 + row.Tourney1 + 1600,
             "Apps": 3,
             "TP": row.T4P + row.T3P + row.T2P + row.T1P,
             "TF": row.T4F + row.T3F + row.T2F + row.T1F,
             "TC": row.T4C + row.T3C + row.T2C + row.T1C} for row in rows if row.Tourney4 != 0]
    return render_template("rank1.html", rows=list)


@app.route('/rulesof45')
def rules_of_45():
    return render_template("rulesof45.html")


@app.route('/links')
def links():
    return render_template("links.html")


@app.route('/happenings')
def happenings():
    return render_template("happenings.html")


@app.route('/display/<event>/<pic>')
def display(event, pic):
    picture = Pictures.query.filter_by(Number=pic, Event=event).first()
    if picture:
        comment = picture.Comment
        filename = "/graphics/" + event + "/" + picture.File
        title = picture.ETitle
        next = int(pic) + 1
        prior = int(pic) - 1
        last = len(Pictures.query.filter_by(Event=event).all())
        return render_template("display.html", event=event, title=title, comment=comment, filename=filename, next=next,
                               prior=prior, last=last, pic=int(pic))
    return abort(404)


@app.route('/karaoke')
def karaoke():
    return render_template("karaoke.html")


@app.route('/luau')
def luau():
    return render_template("luau.html")


@app.route('/fiesta')
def fiesta():
    return render_template("fiesta.html")


@app.route('/mardigras')
def mardigras():
    return render_template("mardigras.html")


@app.route('/fiestalist')
def fiestalist():
    return render_template("fiestalist.html")


@app.route('/luaumusic')
def luaumusic():
    return render_template("luaumusic.html")


@app.route('/mardigraslist')
def mardigraslist():
    return render_template("mardigraslist.html")


@app.route('/serpawedding')
def serpa_wedding():
    return render_template("serpawedding.html")


@app.route('/luncheon1')
def luncheon1():
    return render_template("luncheon1.html")


@app.route('/newyear')
def newyear():
    return render_template("newyear.html")


@app.route('/tnt')
def tnt():
    return render_template("tnt.html")


if __name__ == "__main__":
    app.run(host='127.0.0.29', port=5000, debug=True)
