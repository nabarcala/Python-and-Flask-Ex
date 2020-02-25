# Routes module
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

# Index/Home 
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Natacha'}
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
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # Accept and validate the data, then redirect if valid
    if form.validate_on_submit():
        flash('Login requested for user {}, remember me={}'.format(
        form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    
    return render_template('login.html', title='Sign In', form=form)
