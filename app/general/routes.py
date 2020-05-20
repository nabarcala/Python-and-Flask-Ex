from flask import Blueprint

from flask import render_template, flash, redirect, url_for, request, jsonify
from werkzeug.urls import url_parse
from datetime import datetime

from app import app, db
from app.models import User, Projects
import utils

general = Blueprint('general', __name__,
                   template_folder='templates')


@general.route('/', methods=['GET', 'POST'])
@general.route('/home', methods=['GET', 'POST'])
def home():
    """
    Home page
    """
    projects = Projects.query.limit(6).all()
    software_projects = Projects.query.filter_by(type='software').limit(6).all()
    art_projects = Projects.query.filter_by(type='art').limit(6).all()
    latest_projects = Projects.query.filter_by(type='latest').limit(6).all()
    upcoming_projects = Projects.query.filter_by(type='upcoming').limit(6).all()

    admin = User.query.get(1)
    return render_template('general/home.html', projects=projects, 
        software_projects=software_projects, art_projects=art_projects, 
        latest_projects=latest_projects, upcoming_projects=upcoming_projects, 
        title='Welcome', admin=admin)

@general.route('/update', methods=['POST'])
def update():
    """
    Update the page based on the type of project selected.
    """
    projects = Projects.query.filter_by(id=request.form['id'])
    return jsonify({'results' : 'success'})

# @general.route('/portfolio')
# def portfolio():
#     projects = Projects.query.all()
#     heading = "Portfolio"
#     paths = {
#         "detail": "portfolio",
#         "edit": "edit",
#         "delete": "delete",
#         "moveup": "moveup"
#     }
#     return render_template('general/portfolio.html', title='Portfolio', projects=projects, paths=paths, heading=heading)

# @general.route('/portfolio/<title>')
# def project(title):
#     project = Projects.query.filter_by(title=title).first()
#     if not project:
#         abort(404)
#     go_back = url_for('general.portfolio')
#     return render_template('general/project.html', title='project.tltle', project=project, go_back=go_back)

