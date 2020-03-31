from flask import Blueprint

from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from datetime import datetime

from app import app, db
from app.models import User, Projects

general = Blueprint('general', __name__,
                   template_folder='templates')


@general.route('/', methods=['GET', 'POST'])
@general.route('/home', methods=['GET', 'POST'])
def home():
    admin = User.query.get(1)
    return render_template('general/home.html', title='Welcome', admin=admin)

@general.route('/portfolio')
def portfolio():
    projects = Projects.query.all()
    heading = "Portfolio"
    paths = {
        "detail": "portfolio",
        "edit": "edit",
        "delete": "delete",
        "moveup": "moveup"
    }
    return render_template('general/portfolio.html', title='Portfolio', projects=projects, paths=paths, heading=heading)

@general.route('/portfolio/<title>')
def project(title):
    project = Projects.query.filter_by(title=title).first()
    if not project:
        abort(404)
    go_back = url_for('general.portfolio')
    return render_template('general/project.html', title='project.tltle', project=project, go_back=go_back)

