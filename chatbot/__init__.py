from flask import Flask
from flask_bcrypt import Bcrypt
from .secret import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


bcrypt = Bcrypt(app)

from chatbot import routes
