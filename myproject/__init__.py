import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import openai
import config

openai.api_key = config.api_key

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

def get_completion(prompt, model="gpt-3.5-turbo", temperature=0.6):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def use_word(word):
    prompt = f"""Use the word "{word}" as it appears in a short sentence.""".format(word.capitalize())
    return get_completion(prompt)

app.jinja_env.globals.update(use_word=use_word)
