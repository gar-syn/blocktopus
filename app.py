#!flask/bin/python
import os

from flask import Flask, render_template
from whitenoise import WhiteNoise
from webapp import app

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0:",debug=True)