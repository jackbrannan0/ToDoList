from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import secrets
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__) # Flask instance
app.secret_key = os.environ.get('SECRET_KEY')
print(app.secret_key) # Key needed for flask pop-up messages
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///database.db'
db = SQLAlchemy(app)


import app.routes as routes
from app.models import User






