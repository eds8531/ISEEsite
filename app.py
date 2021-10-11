from myproject import app, db
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user
#from myproject.models import User
#from myproject.site.forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug = True)
