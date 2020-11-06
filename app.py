#
# Copyright (c) 2019 Andrea Fioraldi <andreafioraldi@gmail.com>
# This code is under the BSD 2-clause license
#
# Code inspired by https://github.com/abdesslem/CTF (Copyright (c) 2015 Amri Abdesslem)
#

from flask import Flask, render_template, redirect, url_for, flash, session, abort, request
from flask_security import Security
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import desc
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import Required, Length, EqualTo, Email
from flask_wtf.csrf import CSRFProtect

import datetime
import os
import time
import pytz

################################
#########   GLOBALS   ##########
################################

MAX_SCORE = 100
MIN_SCORE = 20
RATE_SCORE = 2

app = Flask(__name__)
app.config["SECRET_KEY"] = '0000000000000000000000000'
app.config["SECURITY_PASSWORD_SALT"] = '0000000000000'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite')
#app.config["PREFERRED_URL_SCHEME"] = 'https' #decomment for HTTPS
CSRFProtect(app)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

tz = pytz.timezone("Asia/Kolkata")
starttime = datetime.datetime(2020, 11, 6, hour=18, minute=39)
endtime = datetime.datetime(2020, 11, 8, hour=18, minute=47)

################################
##########   MODELS   ##########
################################

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True} 
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80))
    password_hash = db.Column(db.String(120))
    level = db.Column(db.Integer)
    lastSubmit = db.Column(db.DateTime)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

class Challenges(db.Model):
    __tablename__ = 'challenges'
    __table_args__ = {'extend_existing': True}
    
    level = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(80), unique=True)
    #category = db.Column(db.String(60))
    info = db.Column(db.String(1000))
    #score = db.Column(db.String(20))
    flag = db.Column(db.String(80))
    solves = db.Column(db.String(20))

    def __repr__(self):
        return '<Challenge Level {}>'.format(self.level)


"""
def user_score(user):
    solved = user.solved.split(",")
    score = 0
    for c in solved:
        if len(c) == 0: continue
        q = Challenges.query.get(int(c))
        if q is None: continue
        score += int(q.score)
    return score

@app.context_processor
def utility_processor():
    return dict(user_score=user_score)
"""

################################
###########  FORMS   ###########
################################

class LoginForm(FlaskForm):
    login = StringField('Username', validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Login')

class ChallengeForm(FlaskForm):
    flag = StringField('The Flag', validators=[Required(), Length(1, 64)])
    submit = SubmitField('Send')

class RegistrationForm(FlaskForm):
    login = StringField('Username', validators=[Required()])
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    password_again = PasswordField('Password again',
                                   validators=[Required(), EqualTo('password')])
    submit = SubmitField('Register')

def get_hms(delta):
    seconds = delta.seconds
    hours = seconds // 3600
    seconds -= hours * 3600
    minutes = seconds // 60
    seconds -= minutes * 60
    return hours, minutes, seconds
    
################################
##########  ROUTES   ###########
################################

@login_manager.user_loader
def load_user(user_id):
    """User loader callback for Flask-Login."""
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve',methods=["GET","POST"])
@login_required
def solve():
    timenow = datetime.datetime.now()
    if timenow <= starttime:
        delta = starttime - timenow
        hours, minutes, seconds = get_hms(delta)
        return render_template("startsin.html", hours=hours,
                minutes=minutes, seconds=seconds)

    if timenow >= endtime:
        return render_template("ended.html")

    if current_user.level == len(Challenges.query.all()):
        return "You Won!"

    form = ChallengeForm(request.form)
    challenge = Challenges.query.filter_by(level = current_user.level).first()
    #challenge = Challenges.query.filter_by(name=challenge_name).first()
    
    if form.validate_on_submit() and challenge.flag == form.flag.data:
        user = User.query.filter_by(username=current_user.username).first()

        """
        if str(challenge.level) in user.solved.split(","):
            return "Ehi! You can't submit two times the same flag!"
        user.solved = user.solved + ',' + str(challenge.id)
        """

        user.lastSubmit = datetime.datetime.utcnow()
        challenge.solves = str(int(challenge.solves) +1)
        user.level += 1
        db.session.commit()

        return redirect(url_for("solve"))

    elif form.validate_on_submit() and challenge.flag != form.flag.data :
        return render_template("challenge.html", form=form, challenge=challenge,
                wrong=True)
    
    delta = endtime - timenow
    hours, minutes, seconds = get_hms(delta)
    return render_template('challenge.html',form=form, challenge=challenge,
            hours=hours, minutes=minutes, seconds=seconds)

@app.route('/scoreboard')
@login_required
def scoreboard():
    users = User.query.filter(User.username!='admin').all()
    users.sort(key=lambda x: x.level, reverse=True)
    #ranking = -1 if current_user.username == "admin" else int(users.index(current_user)) + 1
    ranking = users.index(current_user)
    return render_template('scoreboard.html', users=users, ranking=ranking)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.login.data).first()
        if user is not None:
            return 'Username already exists.'
        user = User(username=form.login.data,
                       email=form.email.data,
                       password=form.password.data,
                       level=0)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.login.data).first()
        if user is None or not user.verify_password(form.password.data):
            return 'Invalid username or password'
         
        login_user(user)
        return redirect(url_for('index'))
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
