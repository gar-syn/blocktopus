from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from ..models import User, Projects
from .. import db

forms = Blueprint('forms', __name__)

@forms.route('/create-project', methods=['GET', 'POST'])
def create_project():
    from ..form_validation import CreateProject, stringdate
    create_project_form = CreateProject()
    if create_project_form.validate_on_submit():
        guid = request.form['guid']
        title = request.form['title']
        description = request.form['description']
        created_date = stringdate()
        
        create_new_project = Projects(guid, title, description, created_date)
        db.session.add(create_new_project)
        db.session.commit()
        
        message = f"The data for the new project '{title}' with the GUID: {guid} has been submitted."
        return render_template('forms/create-project.html', message=message)
    else:
        # show validaton errors
        for field, errors in create_project_form.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(create_project_form, field).label.text,
                    error
                ), 'error')
        return render_template('forms/create-project.html', create_project_form=create_project_form)
