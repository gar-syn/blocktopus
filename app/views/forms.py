from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_required
from datetime import date
import uuid

from ..models import Projects, Experiments
from .. import db
from ..form_validation import CreateProject, CreateExperiment

forms = Blueprint("forms", __name__)

def stringdate():
    today = date.today()
    date_list = str(today).split('-')
    date_string = date_list[2] + "." + date_list[1] + "." + date_list[0]
    return date_string

@forms.route("/create-project", methods=["GET", "POST"])
@login_required
def create_project():
    create_project_form = CreateProject()
    if create_project_form.validate_on_submit():
        guid = str(uuid.uuid4())
        title = request.form["title"]
        description = request.form["description"]
        created_date = stringdate()
        create_new_project = Projects(guid, title, description, created_date)

        try:
            db.session.add(create_new_project)
            db.session.commit()
            success_message = f"New project '{title}' has been created."
            return render_template("forms/create-project.html", message=success_message)
        except IntegrityError:
            db.session.rollback()
            flash("GUID is already linked to an existing Project!" , 'danger')
            return render_template("forms/create-project.html", create_project_form=create_project_form)
    else:
        # show validaton errors
        for field, errors in create_project_form.errors.items():
            for error in errors:
                flash(
                    "Error in '{}': {}".format(
                        getattr(create_project_form, field).label.text, error
                    ),
                    "error",
                )
        return render_template("forms/create-project.html", create_project_form=create_project_form)
        
@forms.route("/create-experiment", methods=["GET", "POST"])
@login_required
def create_experiment():
    create_experiment_form = CreateExperiment()
    if create_experiment_form.validate_on_submit():
        guid = str(uuid.uuid4())
        eln = request.form["eln"]
        title = request.form["title"]
        description = request.form["description"]
        site = request.form["site"]
        building = request.form["building"]
        room = request.form["room"]
        user_id = current_user.id
        created_date = stringdate()
        last_modified_date = stringdate()
        select_project_guid = request.args.get('project-guid', default = '*', type = str)
        create_new_experiment = Experiments(guid, eln, title, description, site, building, room, user_id, created_date, last_modified_date, select_project_guid)
        try:
            db.session.add(create_new_experiment)
            db.session.commit()
            success_message = f"New experiment '{title}' has been created."
            return render_template("forms/create-experiment.html", message=success_message)
        except IntegrityError:
            db.session.rollback()
            flash("ELN Number is already linked to an existing Project!" , 'danger')
            return render_template("forms/create-experiment.html", create_experiment_form=create_experiment_form)
    #Autopopulate fields, if user is logged in
    elif request.method == 'GET' and current_user.is_authenticated:
        create_experiment_form.site.data = current_user.site
        create_experiment_form.building.data = current_user.building
        create_experiment_form.room.data = current_user.room
        return render_template("forms/create-experiment.html", create_experiment_form=create_experiment_form)
    else:
        for field, errors in create_experiment_form.errors.items():
            for error in errors:
                flash(
                    "Error in '{}': {}".format(
                        getattr(create_experiment_form, field).label.text, error
                    ),
                    "error",
                )
        return render_template("forms/create-experiment.html", create_experiment_form=create_experiment_form)

@forms.route('/projects/<string:id>/delete/', methods=('POST', 'GET'))
def delete_project(id):
    project = Projects.query.get_or_404(id)
    try:
        db.session.delete(project)
        db.session.commit()
        flash('You have successfully deleted the project!', 'success')
        return redirect(url_for('queries.projects'))
    except IntegrityError:
        db.session.rollback()
        flash("You can't delete this project, because there are experiments linked to it!" , 'danger')
        return redirect(url_for('queries.projects'))
    
def save_changes(project, form, new=False):
    project.guid = form.guid.data
    project.title = form.title.data
    project.description = form.description.data
    project.created_date = form.created_date.data
    if new:
        db.session.add(project)
    db.session.commit()
    
@forms.route('/projects/<string:id>/edit/', methods=['GET', 'POST'])
def edit_project(id):
    qry = db.session.query(Projects).filter(Projects.guid==id)
    project = qry.first()
    if project:
        create_project_form = CreateProject(formdata=request.form, obj=project)
        if request.method == 'POST' and create_project_form.validate():
            # save edits
            save_changes(project, create_project_form)
            flash('Project updated successfully!', 'success')
            return redirect(url_for('queries.projects'))
        return render_template('forms/create-project.html', create_project_form=create_project_form)
    else:
        return 'Error loading Project with #{guid}'.format(guid=id)
