import os
from flask import Flask
from whitenoise import WhiteNoise

app = Flask(__name__)
app.config.from_pyfile('config.py') 

static_dir = os.path.join(os.path.dirname(__file__), 'static')
app.wsgi_app = WhiteNoise(app.wsgi_app, root=static_dir, prefix='static/')

from webapp import views