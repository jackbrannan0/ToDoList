from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import secrets



app = Flask(__name__) # Flask instance
app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
print(app.secret_key) # Key needed for flask pop-up messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


import app.routes as routes






