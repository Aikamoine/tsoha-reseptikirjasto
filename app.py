from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import redirect, render_template, request, session

#load_dotenv()
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes
