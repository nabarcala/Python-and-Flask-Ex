from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

from app import app, db
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User, Projects
from app.email import send_password_reset_email
#from app.auth.utils import before_request

auth = Blueprint('auth', __name__,
                   template_folder='templates')


@auth.before_request
def before_request():
    """
    Before before_request
    """
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Admin/User login
    """
    # Redirect if user is logged in already
    if current_user.is_authenticated:
        return redirect(url_for('general.home'))
    form = LoginForm()
    # Accept and validate the data, then redirect if valid
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # Check if password is correct
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        # If passes check, log user in
        login_user(user, remember=form.remember_me.data)
        if user.is_admin:
            return redirect(url_for('admin.admin_dashboard'))
        else:
            # If user has logged in, redirect user to page they were trying to access
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('general.home')
            return redirect(url_for('general.home'))

    return render_template('auth/login.html', title='Sign In', form=form)


@auth.route('/logout')
def logout():
    """
    Logout user
    """
    logout_user()
    return redirect(url_for('general.home'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register a user.
    is_admin is false as default.
    """
    # Check if user is logged in already
    if current_user.is_authenticated:
        return redirect(url_for('general.home'))
    # register the new user
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """
    Reset password request
    """
    if current_user.is_authenticated:
        return redirect(url_for('general.home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    reset password
    """
    if current_user.is_authenticated:
        return redirect(url_for('general.home'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('general.home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
