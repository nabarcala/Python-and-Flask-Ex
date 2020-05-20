from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User, Projects

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

# Form to create posts
# class PostForm(FlaskForm):
#     post = TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=140)])
#     submit = SubmitField('Submit')

class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=140)])
#    imgfile = FileField('Card Image')
    website = StringField('Website')
    github_url =StringField('GitHub Link')
    description = StringField('Description', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Submit')

class EditProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=140)])
    imgfile = FileField('Card Image')
    website = StringField('Website')
    github_url =StringField('GitHub Link')
    description = StringField('Description', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Submit')

    def validate_title(self, title):
        if title.data != self.original_title:
            project = Projects.query.filter_by(title=self.title.data).first()
            if project is not None:
                raise ValidationError('Please use a different title.')
