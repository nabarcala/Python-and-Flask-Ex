# Routes module
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm, ProjectForm
from app.models import User, Post, Projects
from app.email import send_password_reset_email
from werkzeug.urls import url_parse
from datetime import datetime

# Index/Home 
#@app.route('/', methods=['GET', 'POST'])
#@app.route('/index', methods=['GET', 'POST'])
#@login_required
#def index():
#    form = PostForm()
#    if form.validate_on_submit():
#        post = Post(body=form.post.data, author=current_user)
#        db.session.add(post)
#        db.session.commit()
#        flash('Your post is now live!')
#        return redirect(url_for('index'))
#    page = request.args.get('page', 1, type=int)
#    posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
#    next_url = url_for('index', page=posts.next_num) \
#        if posts.has_next else None
#    prev_url = url_for('index', page=posts.prev_num) \
#        if posts.has_prev else None
#    return render_template('index.html', title='Home', form=form, posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='Welcome')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect if user is logged in already
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
            next_page = url_for('home')
        return redirect(url_for('home'))
    
    return render_template('login.html', title='Sign In', form=form)

# Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Register 
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Check if user is logged in already
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)

# Keep track of the last seen
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# Ability to edit profile
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('home'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('home'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))

# Explore page to find others users.
# Uses the index template but not the form argument so that the post form is not included.
@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("index.html", title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/portfolio')
def portfolio():
    projects = Projects.query.all()
    heading = "Portfolio"
    paths = {
        "detail": "portfolio",
        "edit": "edit",
        "delete": "delete",
        "moveup": "moveup"
    }
    return render_template('portfolio.html', title='Portfolio', projects=projects, paths=paths, heading=heading)

@app.route('/portfolio/<title>')
def project(title):
    project = Projects.query.filter_by(title=title).first()
    if not project:
        abort(404)
    go_back = url_for('portfolio')
    return render_template('project.html', title='project.tltle', project=project, go_back=go_back)

@app.route('/portfolio/new_project', methods=['GET', 'POST'])
@login_required
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():
        projects = Projects(
            title = form.title.data,
#            imgfile = form.imgfile.data,
            website = form.website.data,
            github_url = form.github_url.data,
            description = form.description.data
        )
        db.session.add(projects)
        db.session.commit()
        flash('Your project post is now live!')
        return redirect(url_for('portfolio'))
#    else:
#        flash('Project creation failed.')
    return render_template('edit_project.html', form=form, title='Create a Project')