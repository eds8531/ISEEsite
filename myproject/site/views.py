from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from myproject import db, app
from myproject.site.forms import LoginForm, RegistrationForm, SettingsForm
from myproject.models import Student
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import current_user


site_blueprint = Blueprint('site', __name__, template_folder = 'templates/site')

#@site_blueprint.route('/')
#def index():
#    return "<h1>Welcome to the Home Page!</h1>"

# @site_blueprint.route('/register', methods = ['GET','POST'])
# def register():
#     form = RegistrationForm()
#
#     if form.validate_on_submit():
#         email = form.email.data
#         username = form.username.data
#         password = form.password.data
#         new_student = Student(email, username, password)
#         db.session.add(new_student)
#         db.session.commit()
#
#         return redirect(url_for('site.login'))
#
#     return render_template('register.html', form = form)

# There's a better way to do this todays_list function.
# I could call the words directly from the dataframe in SQL.


@site_blueprint.route('/register', methods = ['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        student = Student(email = form.email.data, username = form.username.data, password = form.password.data)
        db.session.add(student)
        db.session.commit()
        flash("Thanks for registering!")
        return redirect(url_for('site.login'))
    return render_template('register.html', form=form)

@site_blueprint.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email = form.email.data).first()

        if student.check_password(form.password.data) and student is not None:

            login_user(student, remember = True)
            flash('Log in successful')

            #Ok. Here is where we want to instantiate todays_list. Fingers crossed.
            current_user.todays_list_inst(current_user.words_a_day)

            # This is pretty cool.
            # It goes back and finds the page the user was looking for before
            # they logged in, retrieves is and sends the user there.
            next= request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('welcome_user')

            return redirect(next)

    return render_template('login.html', form = form)

@site_blueprint.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@site_blueprint.route('/settings', methods = ['GET','POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(username = current_user.username).first()
        new_words_a_day = form.words_a_day.data
        student.words_a_day = new_words_a_day
        #._get_current_object()
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('site.todays_list'))

    return render_template('settings.html', form = form)

@site_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You Logged Out!')
    return redirect(url_for('index'))



@site_blueprint.route('/todays_list')
@login_required
def todays_list():
    todays_list = current_user.todays_list()
    return render_template('Todays_list.html', todays_list = todays_list)

@site_blueprint.route('/flashcards')
@login_required
def flashcards():
    #This is just a placeholder now. The cards don't do anything yet.
    todays_list = current_user.todays_list()
    return render_template('Flashcards.html', todays_list = todays_list)

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')
