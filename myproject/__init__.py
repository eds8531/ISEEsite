import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager  = LoginManager()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db  =SQLAlchemy(app)
Migrate(app,db)

#from myproject.api.views import api_blueprint
from myproject.site.views import site_blueprint

#app.register_blueprint(api_blueprint, url_prefix = '/api')
app.register_blueprint(site_blueprint, url_prefix = '/site')

login_manager.init_app(app)

login_manager.login_view = 'login'
