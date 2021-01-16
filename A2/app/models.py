from datetime import datetime
from app import db
from app import login
from app import admin
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from flask_admin.contrib.sqla import ModelView


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    company = db.Column(db.String(64), index=True)
    contact_no = db.Column(db.Integer(), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    is_admin = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer(), default= 0)
    downloads = db.Column(db.Integer(), default = 0)
    last_seen = db.Column(db.DateTime, default= datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    #uses gravatar service to generate a unique avatar for each user.  MD5 hash is generated from users email address in lowercase,
    #returns a formatted avatar unique to that user with a size specifed as a paramater
    def avatar(self, size): 
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return  'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def update_views(self):
      self.views += 1
      db.session.commit()

    def update_downloads(self):
        self.downloads += 1
        db.session.commit()

      
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    rating = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime(), index=True, 
    default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post> {}>'.format(self.body)


class myUserView(ModelView):  #Overrides Flask Admin model view so I can change class method is_accessible to True only if user is admin. Prevents unauthorised access
    def is_accessible(self):
        if current_user.is_admin:
            return True
        return False
    column_list = ('first_name', 'last_name', 'username', 'company', 'contact_no', 'email', 'is_admin', 'views', 'downloads') #What columns to show
    column_filters= ('first_name', 'username', 'company', 'email', ) #Columns that can be filtered by
    form_excluded_columns =('password_hash') #Excludes password hash from appearing 
    form_widget_args= { #Makes these columns read only so they can't be changed
        'first_name': 
        {
            'readonly': True
        },
        'last_name': 
        {
            'readonly': True
        },
        'username': 
        {
            'readonly': True
        },
        'company': 
        {
            'readonly': True
        },
        'contact_no': 
        {
            'readonly': True
        },
        'views': 
        {
            'readonly': True
        },
        'downloads': 
        {
            'readonly': True
        },
        'email': 
        {
            'readonly': True
        },
        'about_me': 
        {
            'readonly': True
        },
        'last_seen': 
        {
            'readonly': True
        }
    }

 #Adds my adjusted model view to the Admin instances, and specifie what models I can view e.g User model
admin.add_view(myUserView(User, db.session))






