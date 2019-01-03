import os
from flask import Flask, render_template, url_for, views
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

lm = LoginManager() 


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,"noter.db")
app.config['SECRET_KEY'] = "i-love-my-india"
db = SQLAlchemy(app)
lm.init_app(app)
lm.session_protection = 'strong'
lm.loginview = "login"

from .views import *