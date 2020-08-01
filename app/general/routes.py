from flask import Blueprint

from flask import render_template, flash, redirect, url_for, request, jsonify
from werkzeug.urls import url_parse
from datetime import datetime

from app import db
from app.models import User, Projects
# import utils

general = Blueprint('general', __name__,
                   template_folder='templates')


@general.route('/', methods=['GET', 'POST'])
@general.route('/home', methods=['GET', 'POST'])
def home():
    """
    Home page 
    """
    projects = Projects.query.limit(6).all()
    # all_skills = Projects.query.with_entities(Projects.skills).first()
    # skill_list = all_skills.skills.split(", ")
    admin = User.query.get(1)

    # return render_template('general/home.html', projects=projects, skills=skill_list, 
    #     title='Welcome', admin=admin)

        return render_template('general/home.html', projects=projects, 
        title='Welcome', admin=admin)

@general.route('/project/<int:id>', methods=['GET', 'POST'])
def project(id):
    """
    Display a specific project's information 
    """
    project = Projects.query.get(id)
    return render_template('general/project_info.html', project=project)
