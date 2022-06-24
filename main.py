import requests as requests
from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from random import choice
import os
from forms import CreateNewsPostForm, CreateEventForm, LoginForm, FflSeasonUploadForm
import pprint
import csv
from werkzeug.utils import secure_filename
import pandas

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///database/copah.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(member_name):
    return Members.query.get(member_name)


class News(db.Model):
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True)
    # author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # author = relationship("User", back_populates="posts")
    title = db.Column(db.String(250), nullable=False)
    blurb = db.Column(db.String(250))
    date = db.Column(db.String(250), nullable=False)
    news = db.Column(db.Text, nullable=False)
    alias = db.Column(db.String(40), nullable=False)


class Members(UserMixin, db.Model):
    __tablename__ = "members"
    first_name = db.Column(db.String(250))
    last_name = db.Column(db.String(250))
    alias = db.Column(db.String(250))
    college_major = db.Column(db.String(250))
    birthday = db.Column(db.String(250))
    address = db.Column(db.String(250))
    address2 = db.Column(db.String(250))
    city = db.Column(db.String(250))
    state = db.Column(db.String(2))
    zip = db.Column(db.String(10))
    mobile_phone = db.Column(db.String(250))
    home_phone = db.Column(db.String(250))
    email = db.Column(db.String(250))
    work = db.Column(db.String(250))
    site_url = db.Column(db.String(250))
    site_name = db.Column(db.String(250))
    member_name = db.Column(db.String(250), primary_key=True)
    password = db.Column(db.String(250))
    picture = db.Column(db.String(250))
    luncheon_2000 = db.Column(db.Integer())
    friend = db.Column(db.Integer())
    football = db.Column(db.Integer())
    basketball = db.Column(db.Integer())
    hockey = db.Column(db.Integer())
    owner = db.Column(db.String(250))
    baseball = db.Column(db.Integer())
    guests = db.Column(db.Integer())
    cn = db.Column(db.String(250))

    def get_id(self):
        return self.member_name


class Pictures(db.Model):
    __tablename__ = "pictures"
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(100), nullable=False)
    file = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text)
    rating = db.Column(db.Integer(), nullable=False)
    number = db.Column(db.Integer(), nullable=False)
    event_title = db.Column(db.String(250), nullable=False)


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


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(100))
    date = db.Column(db.String(20))
    thumbnail = db.Column(db.String(100))
    picture_key = db.Column(db.String(100))
    location = db.Column(db.String(100))
    body = db.Column(db.Text)


class FflOwner(db.Model):
    __tablename__ = "ffl_owners"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    active = db.Column(db.Boolean)
    seasons = relationship("FflSeason", back_populates="owner")


class FflSeason(db.Model):
    __tablename__ = "ffl_seasons"
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("ffl_owners.id"))
    owner = relationship("FflOwner", back_populates="seasons")
    team = db.Column(db.String(30), nullable=False)
    wins = db.Column(db.Integer, nullable=False)
    losses = db.Column(db.Integer, nullable=False)
    ties = db.Column(db.Integer, nullable=False)
    win_percentage = db.Column(db.Float, nullable=False)
    points_for = db.Column(db.Float, nullable=False)
    points_against = db.Column(db.Float, nullable=False)
    differential = db.Column(db.Float, nullable=False)
    moves = db.Column(db.Integer, nullable=False)
    playoffs = db.Column(db.Boolean)
    runner_up = db.Column(db.Boolean)
    champion = db.Column(db.Boolean)


db.create_all()


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.alias != "Dave":
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def home():
    news = News.query.order_by(News.id.desc()).all()[:5]
    random_picture = choice(Pictures.query.filter_by(rating=0).all())
    photofilename = "graphics/" + random_picture.event + "/" + random_picture.file
    return render_template("index.html", news=news, photo=random_picture, photo_filename=photofilename,
                           current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = Members.query.filter_by(member_name=username).first()

        if not user:
            flash("That member does not exist")
            return redirect(url_for('login'))


        elif user.password != password:
            flash("Password incorrect, please try again.")
            return redirect(url_for('login'))

        else:
            login_user(user, force=True)
            flash('You were successfully logged in')
            return redirect(url_for('home'))
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/members')
def members():
    members = Members.query.filter_by(friend=0).order_by(Members.alias).all()
    return render_template("people.html", members=members)


@app.route('/member/<AKA>')
@login_required
def show_member(AKA):
    member = Members.query.filter_by(alias=AKA).first()
    return render_template("member_profile.html", member=member)


@app.route('/add_event', methods=["GET", "POST"])
@login_required
def add_event():
    list = [""]
    for event in db.session.query(Pictures.event).distinct():
        list.append(event.event)
    form = CreateEventForm()
    form.picture_key.choices = list
    if form.validate_on_submit():
        new_event = Event(
            name=form.name.data,
            type=form.type.data,
            date=form.date.data,
            thumbnail=form.thumbnail.data,
            picture_key=form.picture_key.data,
            location=form.location.data,
            body=form.body.data,
        )
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add_event.html", form=form)


@app.route('/football_upload', methods=["GET", "POST"])
@admin_only
def football_upload():
    # ''' used to upload files'''
    form = FflSeasonUploadForm()
    form.year.choices = list(range(2001, int(date.today().year) + 1))
    # TODO add a check to weed out entries that have already been uploaded
    if form.validate_on_submit():
        uploaded_file = form.file.data

        if uploaded_file.filename:
            file_path = os.path.join("uploads/ffl_seasons", uploaded_file.filename)
            uploaded_file.save(file_path)

            csv_data = open(file_path)
            csvreader = csv.reader(csv_data)
            next(csvreader)

            rows = []
            for row in csvreader:
                playoffs = False
                runner_up = False
                champion = False

                if row[10]:
                    playoffs = True
                    if row[10] == "C":
                        champion = True
                    elif row[10] == "R":
                        runner_up = True

                owner = FflOwner.query.filter_by(name=row[0]).first()

                if not owner:
                    new_owner = FflOwner(
                        name=row[0]
                    )
                    db.session.add(new_owner)
                    db.session.commit()
                    owner = FflOwner.query.filter_by(name=row[0]).first()

                new_ffl_season = FflSeason(
                    year=form.year.data,
                    owner=owner,
                    owner_id=owner.id,
                    team=row[1],
                    wins=row[2],
                    losses=row[3],
                    ties=row[4],
                    win_percentage=row[5],
                    points_for=row[6],
                    points_against=row[7],
                    differential=row[8],
                    moves=row[9],
                    playoffs=playoffs,
                    runner_up=runner_up,
                    champion=champion

                )
                db.session.add(new_ffl_season)
                db.session.commit()

        return redirect(url_for('home'))
    return render_template('football_upload.html', form=form)


@app.route('/football_owner/<int:owner_id>')
def football_owner(owner_id):
    owner = FflOwner.query.get(owner_id)
    total = {"years": 0,
             "wins": 0,
             "losses": 0,
             "ties": 0,
             "points_for": 0,
             "points_against": 0,
             "moves": 0,
             "playoffs": 0,
             "runner_up": 0,
             "champion": 0
             }

    for season in owner.seasons:
        total["years"] += 1
        total["wins"] += season.wins
        total["losses"] += season.losses
        total["ties"] += season.ties
        total["points_for"] += season.points_for
        total["points_against"] += season.points_against
        total["moves"] += season.moves

        if season.champion:
            total["champion"] += 1

        if season.playoffs:
            total["playoffs"] += 1

        if season.runner_up:
            total["runner_up"] += 1

    total["points_for"] = round(total["points_for"], 2)
    total["points_against"] = round(total["points_against"], 2)
    total["differential"] = round(total["points_for"] - total["points_against"], 2)

    total["win_percentage"] = round(total["wins"] / (total["wins"] + total["losses"] + total["ties"]), 3)

    return render_template("ffl_owner.html", owner=owner, total=total)


@app.route('/football_owners')
def football_owners():
    owners = FflOwner.query.filter_by(active=True).order_by(FflOwner.name).all()
    return render_template("ffl_owners.html", owners=owners)


@app.route('/football_totals')
def football_totals():
    all_season = FflSeason.query.get_all()
    new_data = pandas.DataFrame()
    new_data.read_sql()
    return render_template("football_totals.html")


@app.route('/view_event/<int:event_id>')
def view_event(event_id):
    event = Event.query.get(event_id)
    pics = Pictures.query.filter_by(event=event.picture_key).all()
    return render_template("view_event.html", event=event, pics=pics)


@app.route('/news_post', methods=["GET", "POST"])
@login_required
def news_post():
    form = CreateNewsPostForm()
    if form.validate_on_submit():
        new_post = News(
            Title=form.title.data,
            Blurb=form.blurb.data,
            News=form.news.data,
            AKA=current_user.alias,
            Date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("newspost.html", form=form)


@app.route('/history/<int:chapter>')
def history(chapter):
    if chapter == 1:
        pages = [0, 1, 2]
    elif chapter == 2:
        pages = [1, 2, 3]
    elif chapter == 3:
        pages = [2, 3, 0]
    print(chapter, pages)
    return render_template("history.html", chapter=chapter, pages=pages)


@app.route('/archives')
def archives():
    news = News.query.order_by(News.id.desc()).all()
    return render_template("index.html", news=news)


@app.route('/gallery')
def gallery():
    return render_template("gallery.html")


@app.route('/tournaments')
def tournaments():
    tournaments = Event.query.filter_by(type="T").all()
    return render_template("tournaments.html", tournaments=tournaments)


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
    list = [{"AKA": row.alias,
             "Pts": row.Tourney1 + 1600,
             "Apps": 1,
             "TP": row.T1P,
             "TF": row.T1F,
             "TC": row.T1C} for row in rows if row.Tourney1 != 0 or row.alias == "Jay-Ave" or row.alias == "Serpentor"]
    return render_template("rank1.html", rows=list)


@app.route('/rank/2')
def rank_2():
    rows = Rank.query.order_by(Rank.Tourney2.desc()).all()
    list = [{"AKA": row.alias,
             "Pts": row.Tourney2 + row.Tourney1 + 1600,
             "Apps": 2,
             "TP": row.T2P + row.T1P,
             "TF": row.T2F + row.T2F,
             "TC": row.T2C + row.T2C} for row in rows if row.Tourney2 != 0]
    return render_template("rank1.html", rows=list)


@app.route('/rank/3')
def rank_3():
    rows = Rank.query.order_by(Rank.Tourney3.desc()).all()
    list = [{"AKA": row.alias,
             "Pts": row.Tourney3 + row.Tourney2 + row.Tourney1 + 1600,
             "Apps": 3,
             "TP": row.T3P + row.T2P + row.T1P,
             "TF": row.T3F + row.T2F + row.T1F,
             "TC": row.T3C + row.T2C + row.T1C} for row in rows if row.Tourney3 != 0]
    return render_template("rank1.html", rows=list)


@app.route('/rank/4')
def rank_4():
    rows = Rank.query.order_by(Rank.Tourney4.desc()).all()
    list = [{"AKA": row.alias,
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
        comment = picture.comment
        filename = "/graphics/" + event + "/" + picture.file
        title = picture.event_title
        next = int(pic) + 1
        prior = int(pic) - 1
        last = len(Pictures.query.filter_by(Event=event).all())
        return render_template("display.html", event=event, title=title, comment=comment, filename=filename, next=next,
                               prior=prior, last=last, pic=int(pic))
    return abort(404)


@app.route('/karaoke')
def karaoke():
    karaokes = Event.query.filter_by(type="K").all()
    return render_template("karaoke.html", karaokes=karaokes)


@app.route('/luau')
def luau():
    return redirect(url_for("view_event", event_id=18))


@app.route('/fiesta')
def fiesta():
    return redirect(url_for("view_event", event_id=21))


@app.route('/mardigras')
def mardigras():
    return redirect(url_for("view_event", event_id=20))


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
