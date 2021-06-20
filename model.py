from enum import auto, unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

from sqlalchemy.orm import *
from settings import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)


class Users(db.Model):

    user_id = db.Column(db.String, primary_key=True, nullable=False)
    username = db.Column(db.String(20),  nullable=False)
    profile_picture = db.Column(db.String, nullable=False)


    def __init__(self, user_id, username, profile_picture):

        self.user_id = user_id
        self.username = username
        self.profile_picture = profile_picture

    def serialize(self):
        return{

            "username": self.username,
            "profile_picture": self.profile_picture,

        }

def create():

    #db.drop_all()
    db.create_all()
    
create()
