# Routes module
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime

# Index/Home 
@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect if user is logged in already
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # Accept and validate the data, then redirect if valid
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # Check if password is correct
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # If passes check, log user in
        login_user(user, remember=form.remember_me.data)
        # If user has logged in, redirect user to page they were trying to access
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    
    return render_template('login.html', title='Sign In', form=form)

# Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Register 
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Check if user is logged in already
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # register the new user
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# User's profile
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

# Keep track of the last seen
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
























