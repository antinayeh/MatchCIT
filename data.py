from typing import Dict
from flask import Flask
from os import path 

import pandas as pd
from config import DB_NAME, sender_email, sender_password


match_result_filename = 'match_result.csv'

def create_app(db):
    app = Flask(__name__, static_folder="./static", template_folder="./")
    app.config['SECRET_KEY'] = 'hello ha'
    
    # Initialize database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Mail
    app.config['MAIL_SERVER']= 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = sender_email
    app.config['MAIL_PASSWORD'] = sender_password
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    return app 


def create_database(app, db):
    if not path.exists(DB_NAME):
        db.create_all(app=app)
        print('create database!')


def read_match_result() -> pd.DataFrame:
    df = pd.read_csv(match_result_filename)
    return df
