from flask import Blueprint

from flask import render_template, flash, redirect, url_for, request, jsonify
from werkzeug.urls import url_parse
from datetime import datetime

from app import db
from app.models import User, Projects
# import utils

import base64

general = Blueprint('general', __name__,
                   template_folder='templates')


@general.route('/', methods=['GET', 'POST'])
@general.route('/home', methods=['GET', 'POST'])
def home():
    """
    Home page 
    """
    skill_list = [0]
    projects = Projects.query.order_by(Projects.id.desc())

    for project in projects:
        item = project.skills.split(", ") 
        skill_list.insert(1, item)
        
    admin = User.query.get(1)

    return render_template('general/home.html', projects=projects, skills=skill_list,
        title='Welcome', admin=admin) 


@general.route('/project/<int:id>', methods=['GET', 'POST']) 
def project(id):
    """
    Display a specific project's information 
    
    """
    project = Projects.query.get(id)
    # imgfile = base64.b64decode(project.imgfile)
    # img_file = Projects.query.with_entities(Projects.imgfile).first()
    return render_template('general/project_info.html', project=project)
