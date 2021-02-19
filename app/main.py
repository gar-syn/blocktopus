from flask import Blueprint, render_template, send_from_directory
from flask_login import login_required, current_user

from . import db

main = Blueprint('main', __name__)

@main.route("/home")
@main.route("/index")
@main.route("/index.html")
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/projects')
def projects():
    return render_template('projects.html')

@main.route('/experiments')
def experiments():
    return render_template('experiments.html')