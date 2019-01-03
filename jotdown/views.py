from flask import flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from . import app, lm
from .models import Note, User
from .forms import LoginForm, SignupForm, AddNoteForm

@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new = User(username=form.username.data, email=form.email.data, password=form.password.data)
        new.save()
        flash("Registration was successful")
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("login successful")
            return redirect(url_for('home'))
        flash("Incorrect password or email")
    return render_template('login.html', form=form)

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_required
@app.route('/home')
def home():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html', notes=notes)

@login_required
@app.route('/add', methods=['POST','GET'])
def add():
    form = AddNoteForm()
    notes = Note.query.filter_by(user_id=current_user.id).all()
    if form.validate_on_submit():
        new = Note(title=form.title.data, content=form.content.data, user_id=current_user.id)
        new.save()
        flash("Note created successfully!")
        return redirect(url_for('home'))
    return render_template('new.html', form=form, notes=notes)

@login_required
@app.route('/view/<id>')
def view(id):
    note = Note.query.get(id)
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('note.html', note=note, notes=notes)

