import os
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
import openpyxl
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from myproject import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime
import datetime





@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(user_id)

class Student(db.Model, UserMixin):

    __tablename__ = 'students'

    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    #age = db.Column(db.Integer)
    email = db.Column(db.String(64), unique = True, index = True)
    wordlist = db.Column(db.String(128))
    words_a_day = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))



    def __init__(self, email, username, password, words_a_day = 20):
        self.username = username
        #self.age = age
        self.email = email
        self.words_a_day = words_a_day
        self.password_hash = generate_password_hash(password)
        wordlist = self.start_wordlist()
        self.wordlist = wordlist

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.user_id

    def start_wordlist(self):
        # I need to make each new wordlist unique to it's user.
        df = pd.read_excel('myproject/wordlists/ISEEWords1 3.xlsx', parse_dates = ['Date'])
        wordlist = os.path.join(current_app.root_path, 'wordlists', str(self.username) + 'df.pkl')
        df.to_pickle(wordlist, compression = None)
        return wordlist

    # I need to split the todays_list() function into a function that instantiates a list and one that calls the list the first function made.

    #This is the list that instantiates todays_list at login.
    def todays_list_inst(self, words_a_day):
        #This line of code will need to change to import the user's word list.
        #df = pd.read_pickle(current_app.root_path + 'wordlists/' + str(self.username) + '.pkl')
        df = pd.read_pickle(os.path.join(current_app.root_path, 'wordlists', str(self.username) + 'df.pkl'))

        #The next 4 lines should fix the datetime issues for now, but will probably have to be fixed later.
        #for i in df.index.values:
        #    if df.loc[i,'Date'] != np.nan:
        #        df.loc[i,'Date'] = pd.to_datetime(df.loc[i,'Date'])
        #        df.loc[i,'Date'] = df.loc[i,'Date'].dt.date

        #Mov this line to start wordlist
        df['Date'] = [np.nan] *499
        df1 = df.dropna(subset = ['Date'])
        #I'm worried this next line of code where I write datetime instead of date
        # will cause problems down the road, but for now I'm going with it.
        tdl = df1[df1['Date'] <= datetime.datetime.today()]

        adtl_words = words_a_day - len(tdl)
        #print(df.iloc[5,2].isnull())
        if adtl_words <= 0:
            tdl =  tdl[:words_a_day]

        elif adtl_words > 0:
            df2 = df[df['Date'].isnull()].sample(adtl_words)
            frames = [df1,df2]
            tdl = pd.concat(frames)
            tdl = tdl.sample(len(tdl))

        wordlist = os.path.join(current_app.root_path, 'wordlists', str(self.username) + '_todays_list.pkl')
        tdl.to_pickle(wordlist, compression = None)

    # Here is the function that calls the list made by todays_list_inst().
    def todays_list(self):
        tdl = pd.read_pickle(os.path.join(current_app.root_path, 'wordlists', str(self.username) + '_todays_list.pkl'))
        return tdl





    def __repr__(self):
        return f"{self.username} is a student who is trying to learn {self.words_a_day} words a day."
