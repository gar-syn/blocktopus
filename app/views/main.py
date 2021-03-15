from flask import Blueprint, render_template, send_from_directory, request, redirect, url_for, session

from app.util.extensions import db

main = Blueprint('main', __name__)

def redirect_previous_url(default='main.index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)

@main.route('/language/<language>')
def set_language(language=None):
    session['language'] = language
    return redirect(redirect_previous_url())

@main.route("/home")
@main.route("/index")
@main.route("/index.html")
@main.route('/')
def index():
    return render_template('index.html')