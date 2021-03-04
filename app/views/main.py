from flask import Blueprint, render_template, send_from_directory

from ..util.extensions import db

main = Blueprint('main', __name__)

@main.route("/home")
@main.route("/index")
@main.route("/index.html")
@main.route('/')
def index():
    return render_template('index.html')