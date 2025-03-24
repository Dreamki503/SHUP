from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

from api_key import CLIENT_ID, CLIENT_SECRET

app = Flask(__name__)
login_manager = LoginManager(app)
UPLOAD_FOLDER = 'static/uploads/'
load_dotenv()

password = os.getenv("password")
escaped_password = quote_plus(password)

app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+mysql-connector-python://{os.getenv("user")}:{escaped_password}@{os.getenv("host")}/{os.getenv("database")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("secret_key")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
migrate = Migrate(app, db)
