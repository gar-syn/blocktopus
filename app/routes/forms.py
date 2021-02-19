from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy.exc import IntegrityError
from flask_login import current_user

from ..util.table_queries import DataTable
from ..models import Projects, Experiments
from .. import db
from ..form_validation import CreateProject, CreateExperiment, stringdate

forms = Blueprint("forms", __name__)

@forms.route('/load')
def load():
    if request.method == 'GET':
        ret = DataTable(request, Projects).output_result()
        return jsonify(ret)

@forms.route("/create-project", methods=["GET", "POST"])
def create_project():
    create_project_form = CreateProject()
    if create_project_form.validate_on_submit():
        guid = request.form["guid"]
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
            flash("GUID is already linked to an existing Project!")
            return render_template(
                "forms/create-project.html", create_project_form=create_project_form
            )

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
        return render_template(
            "forms/create-project.html", create_project_form=create_project_form
        )
        
def auto_populate_project_choices_dropdown(create_experiment_form):
    projects = Projects.query.all()
    project_guids = []
    for project in projects:
        project_guids.append(project.guid)
    project_choices = list(project_guids)
    create_experiment_form.select_project_guid.choices = project_choices

@forms.route("/create-experiment", methods=["GET", "POST"])
def create_experiment():
    create_experiment_form = CreateExperiment()
    auto_populate_project_choices_dropdown(create_experiment_form)
    if create_experiment_form.validate_on_submit():
        guid = request.form["guid"]
        eln = request.form["eln"]
        title = request.form["title"]
        description = request.form["description"]
        site = request.form["site"]
        building = request.form["building"]
        room = request.form["room"]
        if current_user.is_authenticated:
            user_id = current_user.id
        else: user_id = 0
        created_date = stringdate()
        last_modified_date = stringdate()
        select_project_guid = create_experiment_form.data['select_project_guid']        
        create_new_experiment = Experiments(guid, eln, title, description, site, building, room, user_id, created_date, last_modified_date, select_project_guid)

        try:
            db.session.add(create_new_experiment)
            db.session.commit()
            success_message = f"New experiment '{title}' has been created."
            return render_template("forms/create-experiment.html", message=success_message)
        except IntegrityError:
            db.session.rollback()
            flash("GUID is already linked to an existing Project!")
            return render_template(
                "forms/create-experiment.html", create_experiment_form=create_experiment_form
            )

    else:
        # show validaton errors
        for field, errors in create_experiment_form.errors.items():
            for error in errors:
                flash(
                    "Error in '{}': {}".format(
                        getattr(create_experiment_form, field).label.text, error
                    ),
                    "error",
                )
        return render_template(
            "forms/create-experiment.html", create_experiment_form=create_experiment_form
        )
