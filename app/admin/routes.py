from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

from app import db
from app.admin.forms import EditProfileForm, ProjectForm, EditDataForm
from app.models import User, Projects
# from app.admin.utils import check_admin

admin = Blueprint('admin', __name__,
                   template_folder='templates')


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


@admin.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """
    Show admin dashboard and prevent non-admins from accessing it.
    Admins can modify data from the dashboard
    """
    if not current_user.is_admin:
        return url_for('404.html')
    return render_template('admin/admin_dashboard.html', title='Dashboard')


@admin.route('/admin/portfolio', methods=['GET', 'POST'])
@login_required
def list_projects():
    """
    List all projects in portfolio
    """
    check_admin()
    projects = Projects.query.all()
    return render_template('admin/projects.html', projects=projects, title="Projects")


@admin.route('/admin/portfolio/add', methods=['GET', 'POST'])
@login_required
def add_project():
    """
    Create a new project to add to the portfolio.
    """
    check_admin()
    add_project = True

    form = ProjectForm()
    if form.validate_on_submit():
        projects = Projects(
            title = form.title.data,
#            imgfile = form.imgfile.data,
            website = form.website.data,
            github_url = form.github_url.data,
            description = form.description.data,
            project_type = form.project_type.data
        )
        try:
            db.session.add(projects)
            db.session.commit()
            flash('Your project post is now live!')
        except:
            flash('Error: project name already exists.')
            return redirect(url_for('portfolio'))

        return redirect(url_for('admin.list_projects'))

    return render_template('admin/project.html', form=form, title='Create a Project', action='Add', add_project=add_project)


@admin.route('/admin/portfolio/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    """
    Edit a project from the portfolio.
    """
    check_admin()
    add_project = False

    project = Projects.query.get_or_404(id)
    form = ProjectForm()
    if form.validate_on_submit():
        project.title = form.title.data
        # imgfile = form.imgfile.data
        project.website = form.website.data
        project.github_url = form.github_url.data
        project.description = form.description.data
        project.project_type = form.project_type.data
        db.session.commit()
        flash('Project has been successfully updated.')
        return redirect(url_for('admin.list_projects'))

    form.title.data = project.title
    form.website.data = project.website
    form.github_url.data = project.github_url
    form.description.data = project.description
    form.project_type.data = project.project_type
    return render_template('admin/edit_form.html', form=form, title='Edit Project', action='Edit', add_project=add_project, project=project)


@admin.route('/admin/portfolio/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_project(id):
    """
    Delete a project from the portfolio.
    """
    check_admin()

    project = Projects.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()

    flash('Project has been successfully deleted.')
    return redirect(url_for('admin.list_projects'))

    return render_template(title='Delete Project')

@admin.route('/admin/data', methods=['GET', 'POST'])
@login_required
def list_data():
    """
    List all the information for the admin to see
    """
    check_admin()
    user = User.query.filter_by(is_admin='1').first()
    return render_template('admin/information.html', admin=user, title="Admin Data")

@admin.route('/admin/data/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_data(id):
    """
    Edit personal data stored in the database
    """
    check_admin()
    edit_data = True

    user = User.query.filter_by(id='1').first()

    form = EditDataForm()
    if form.validate_on_submit():
        user.career = form.career.data
        user.headline = form.headline.data
        user.about_me = form.about_me.data
        db.session.commit()
        flash('Data has been successfully updated.')
        return redirect(url_for('admin.list_data'))

    form.career.data = user.career
    form.headline.data = user.headline
    form.about_me.data = user.about_me
    return render_template('admin/edit_form.html', form=form, title='Edit Data', action='Edit', edit_data=edit_data, admin=user)


#
# @admin.route('/admin/<username>')
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     page = request.args.get('page', 1, type=int)
#     posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
#     next_url = url_for('admin.user', username=user.username, page=posts.next_num) \
#         if posts.has_next else None
#     prev_url = url_for('admin.user', username=user.username, page=posts.prev_num) \
#         if posts.has_prev else None
#     return render_template('admin/user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)
#
# @admin.route('/admin/edit_profile', methods=['GET', 'POST'])
# @login_required
# def edit_profile():
#     form = EditProfileForm(current_user.username)
#     if form.validate_on_submit():
#         current_user.username = form.username.data
#         current_user.about_me = form.about_me.data
#         current_user.headline = form.headline.data
#         current_user.career = form.career.data
#         db.session.commit()
#         flash('Your changes have been saved.')
#         return redirect(url_for('admin.user', username=current_user.username))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.about_me.data = current_user.about_me
#         form.headline.data = current_user.headline
#         form.career.data = current_user.career
#     return render_template('admin/edit_profile.html', title='Edit Profile', form=form)
