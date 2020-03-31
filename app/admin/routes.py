from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

from app import app, db
from app.admin.forms import EditProfileForm, ProjectForm
from app.models import User, Projects
from app.admin.utils import check_admin

admin = Blueprint('admin', __name__,
                   template_folder='templates')


@admin.route('/dashboard')
@login_required
def admin_dashboard():
    """
    Show admin dashboard and prevent non-admins from accessing it.
    Admins can modify data from the dashboard
    """
    if not current_user.is_admin:
        return url_for('404.html')
    return render_template('admin/admin_dashboard.html', title='Dashboard')


@admin.route('/portfolio/add', methods=['GET', 'POST'])
@login_required
def add_project():
    """
    Create a new project to add to the portfolio.
    """
    form = ProjectForm()
    if form.validate_on_submit():
        projects = Projects(
            title = form.title.data,
#            imgfile = form.imgfile.data,
            website = form.website.data,
            github_url = form.github_url.data,
            description = form.description.data
        )
        try:
            db.session.add(projects)
            db.session.commit()
            flash('Your project post is now live!')
        except:
            flash('Error: project name already exists.')
        return redirect(url_for('portfolio'))
#    else:
#        flash('Project creation failed.')
    return render_template('edit_project.html', form=form, title='Create a Project')

@admin.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('admin.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('admin.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('admin/user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)

@admin.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.headline = form.headline.data
        current_user.career = form.career.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('admin.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.headline.data = current_user.headline
        form.career.data = current_user.career
    return render_template('admin/edit_profile.html', title='Edit Profile', form=form)
