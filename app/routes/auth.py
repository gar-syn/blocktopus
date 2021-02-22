from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user


from ..models import User
from .. import db
from ..form_validation import ChangeSite

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET'])
def login():
    print("Login")
    return render_template('auth/login.html')

@auth.route('/register')
def register():
    print("register")
    return render_template('auth/register.html')
    
@auth.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    site = request.form.get('site')
    building = request.form.get('building')
    lab = request.form.get('lab')

    # check for existing user
    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address is already registered' , 'danger')
        return redirect(url_for('auth.register'))

    # create new user
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), site=site, building=building, lab=lab)

    # add to database
    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        return 'Unable to add the user to database.'
    flash('Account has been registered. Please log in:', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists and compare passwords
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', 'danger')
        return redirect(url_for('auth.login'))  # if user doesn't exist or password is wrong, reload the page

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/change-site', methods=['GET', 'POST'])
@login_required
def change_site():
    change_site_form = ChangeSite()
    if request.method == 'POST':
        if change_site_form.validate_on_submit():
            user = current_user
            user.site = change_site_form.site.data
            db.session.add(user)
            db.session.commit()
            flash('Your site has been changed.', 'success')
            return redirect(url_for('main.profile'))
    return render_template('auth/change-site.html', site=current_user.site, change_site_form=change_site_form)
