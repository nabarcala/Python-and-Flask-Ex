import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField, SelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

from app import uploads
from app.models import User, Projects

PROJECT_TYPE = [('SW', 'Software'), ('AR', 'Art'), ('UPC', 'Upcoming')]

class EditProfileForm(FlaskForm):
    career = StringField('Career', validators=[Length(min=0, max=140)])
    headline = TextAreaField('Headline', validators=[Length(min=0, max=400)])
    username = StringField('Username')
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=20)])
    imgfile = FileField('Project Image', validators=[FileRequired(), FileAllowed(uploads, 'Images only!')])
    website = StringField('Website')
    github_url =StringField('GitHub Link')
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=5000)])
    project_type = SelectField(label='Project Type', choices=PROJECT_TYPE)
    submit = SubmitField('Submit')

class EditProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=20)])
    imgfile = FileField('Project Image', validators=[FileRequired(), FileAllowed(uploads, 'Images only!')])
    website = StringField('Website')
    github_url =StringField('GitHub Link')
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=5000)])
    project_type = SelectField(label='Project Type', choices=PROJECT_TYPE)
    submit = SubmitField('Submit')

    def validate_title(self, title):
        if title.data != self.original_title:
            project = Projects.query.filter_by(title=self.title.data).first()
            if project is not None:
                raise ValidationError('Please use a different title.')

class EditDataForm(FlaskForm):
    career = StringField('Career', validators=[DataRequired()])
    headline = TextAreaField('Headline', validators=[Length(min=0, max=140)])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
        
