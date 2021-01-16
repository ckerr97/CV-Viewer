from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_moment import Moment

#creates instances of all of these classes to be used throughout my project

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
admin = Admin(app, template_mode='bootstrap4') #For admin page nav bar
bootstrap = Bootstrap(app)
migrate = Migrate(app, db)
login = LoginManager(app)
moment = Moment(app)  
login.login_view = 'login'

from app import routes, models








