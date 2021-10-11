from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo

from flask_login import current_user
from myproject.models import Student 

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField("Log in")

class RegistrationForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired(), EqualTo('pass_confirm', message = 'Passwords must match')])
    pass_confirm = PasswordField('Confirm Password', validators = [DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self, field):
        if Student.query.filter_by(email =  field.data).first():
            raise ValidationError("This email is already in use.")

    def check_username(self, field):
        if Student.query.filter_by(username =  field.data).first():
            raise ValidationError("This user name is already in use.")

class SettingsForm(FlaskForm):
    words_a_day = IntegerField("How many words would you like to learn a day?")
    submit = SubmitField('Ok')
