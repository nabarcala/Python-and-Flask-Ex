from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_uploads import configure_uploads, IMAGES, UploadSet

from werkzeug.urls import url_parse
from datetime import datetime
import base64
import os

import cloudinary
from cloudinary.api import delete_resources_by_tag, resources_by_tag
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url 
from cloudinary import CloudinaryImage

from app import db, uploads
from app.admin.forms import EditProjectForm, ProjectForm, EditDataForm
from app.models import User, Projects
# from app.admin.utils import check_admin

admin = Blueprint('admin', __name__,
                   template_folder='templates')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = 'app/static/img/uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    imgfile = []
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
        # filename = uploads.save(form.imgfile.data)
        # return filename

        file = form.imgfile.data

        file_split = file.filename.rsplit('.', 1)
        filename = file_split[0]
        file_url_end = "." + file_split[1]



        flash(filename)
        # filename = file.filename
        file_upload_url = os.path.join(UPLOAD_FOLDER, filename)

        # Get image
        if filename == '':
            flash('No image selected.')
            return redirect(url_for('admin.add_project'))
        
        if file and allowed_file(file.filename): 
            file.save(file_upload_url)
            flash('Image successfully uploaded and displayed')

            response = upload ( 
                file_upload_url,
                tags="Project",
                public_id=filename,
            )
            url, options = cloudinary_url(
                response['public_id'],
                format=response['format']
            )

        # Save data to database
        projects = Projects(
            title = form.title.data,

            # imgname = file.filename, 
            # imgfile = file.read(), 
            
            # imgfile = filename,
            imgname = filename, 
            img_urlend = file_url_end,

            website = form.website.data,
            github_url = form.github_url.data,

            description = form.description.data,
            # skills = form.skills.data,
            project_type = form.project_type.data
        )
        try:
            db.session.add(projects)
            db.session.commit()
            flash('Your project post is now live!')
        except:
            flash('Error: project name already exists.')
            return redirect(url_for('admin.add_project'))

        return redirect(url_for('admin.list_projects'))

        # return imgfile.filename

    return render_template('admin/edit_form.html', form=form, title='Create a Project', action='Add', add_project=add_project)


@admin.route('/admin/portfolio/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    """
    Edit a project from the portfolio.
    """
    check_admin()
    add_project = False

    project = Projects.query.get_or_404(id)
    form = EditProjectForm()
    if form.validate_on_submit():
        # project.title = form.title.data
        
        if form.imgfile.data:
            file = form.imgfile.data

            file_split = file.filename.rsplit('.', 1)
            filename = file_split[0]
            file_url_end = "." + file_split[1]

            flash(filename)
            # filename = file.filename
            file_upload_url = os.path.join(UPLOAD_FOLDER, filename)

            # Get image
            
            if file and allowed_file(file.filename): 
                file.save(file_upload_url)
                flash('Image successfully uploaded and displayed')

                response = upload ( 
                    file_upload_url,
                    tags="Project",
                    public_id=filename,
                )
                url, options = cloudinary_url(
                    response['public_id'],
                    format=response['format']
                )

                project.imgname = filename
                project.img_urlend = file_url_end

        project.website = form.website.data
        project.github_url = form.github_url.data
        project.description = form.description.data
        # project.skills = form.skills.data
        project.project_type = form.project_type.data
        db.session.commit()
        flash('Project has been successfully updated.')
        return redirect(url_for('admin.list_projects'))

    form.title.data = project.title

    file = project.imgname + project.img_urlend 
    form.imgfile.data = file


    # form.imgfile.data = project.imgfile
    # form.imgurl.data = project.imgurl
    form.website.data = project.website
    form.github_url.data = project.github_url
    form.description.data = project.description
    # form.skills.data = project.skills
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
