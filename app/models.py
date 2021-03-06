from app import db, login
from datetime import datetime
from time import time
import jwt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from wtforms.validators import Regexp
#from sqlalchemy_utils import URLType

# Followers association table
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    headline = db.Column(db.String(140))
    career = db.Column(db.String(140))
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    
    # How to print objects of this class
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    # Set a hashed password using werkzeug
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # Using Gravatar for user icons
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
    
    # Add and remove follower functions below:
    # def follow(self, user):
    #     if not self.is_following(user):
    #         self.followed.append(user)

    # def unfollow(self, user):
    #     if self.is_following(user):
    #         self.followed.remove(user)

    # def is_following(self, user):
    #     return self.followed.filter(followers.c.followed_id == user.id).count() > 0
    
    # def followed_posts(self):
    #     followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id)
    #     own = Post.query.filter_by(user_id=self.id)
    #     return followed.union(own).order_by(Post.timestamp.desc())
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
    
# Get the user's data using the ID of the user
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True, info={"validators": Regexp("^[A-Za-z0-9_-]*$")})
    imgfile = db.Column(db.LargeBinary) 
    # imgfile = db.Column(db.String(100))
    imgname = db.Column(db.String(100))
    img_urlend = db.Column(db.String(10))
    website = db.Column(db.String(100))
    github_url = db.Column(db.String(100))
    description = db.Column(db.String(5000))
    project_type = db.Column(db.String(3))
    skills = db.Column(db.String(500)) 

    def __repr__(self):
        return '<Project title: {}>'.format(self.title)
