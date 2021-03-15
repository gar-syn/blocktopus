from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_required
from datetime import date, datetime
from flask_babel import _

from app.models.model import Projects, Experiments
from app.util.extensions import db
from app.util.form_validation import CreateProject, CreateExperiment

forms = Blueprint("forms", __name__)

def stringdate():
    today = date.today()
    date_list = str(today).split('-')
    date_string = date_list[2] + "." + date_list[1] + "." + date_list[0]
    return date_string

def stringdatetime():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


@forms.route("/create-project", methods=["GET", "POST"])
@login_required
def create_project():
    create_project_form = CreateProject()
    if create_project_form.validate_on_submit():
        title = request.form["title"]
        description = request.form["description"]
        created_date = stringdate()
        create_new_project = Projects(title, description, created_date)

        try:
            db.session.add(create_new_project)
            db.session.commit()
            success_message = _("New project '%(title)s' has been created.", title=title)
            return render_template("forms/create-project.html", message=success_message)
        except IntegrityError:
            db.session.rollback()
            flash(_('GUID is already linked to an existing Project!'), 'danger')
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
        create_new_experiment = Experiments(eln, title, description, site, building, room, user_id, created_date, last_modified_date, select_project_guid)
        try:
            db.session.add(create_new_experiment)
            db.session.commit()
            success_message = _("New experiment '%(title)s' has been created.", title=title)
            return render_template("forms/create-experiment.html", message=success_message)
        except IntegrityError:
            db.session.rollback()
            flash(_('ELN Number is already linked to an existing Project!'), 'danger')
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
@login_required
def delete_project(id):
    project = Projects.query.get_or_404(id)
    try:
        db.session.delete(project)
        db.session.commit()
        flash(_('You have successfully deleted the project!'), 'success')
        return redirect(url_for('queries.projects'))
    except IntegrityError:
        db.session.rollback()
        flash(_('You can not delete this project, because there are experiments linked to it!') , 'danger')
        return redirect(url_for('queries.projects'))
    
def save_project_changes(project, form, new=False):
    project.title = form.title.data
    project.description = form.description.data
    project.created_date = form.created_date.data
    if new:
        db.session.add(project)
    db.session.commit()
    
@forms.route('/projects/<string:id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    qry = db.session.query(Projects).filter(Projects.id==id)
    project = qry.first()
    if project:
        create_project_form = CreateProject(formdata=request.form, obj=project)
        if request.method == 'POST' and create_project_form.validate():
            save_project_changes(project, create_project_form)
            flash(_('Project updated successfully!'), 'success')
            return redirect(url_for('queries.projects'))
        return render_template('forms/create-project.html', create_project_form=create_project_form)
    else:
        return 'Error loading Project with #{guid}'.format(guid=id)

@forms.route('/experiments/<string:id>/delete/', methods=('POST', 'GET'))
@login_required
def delete_experiment(id):
    experiment = Experiments.query.get_or_404(id)
    try:
        db.session.delete(experiment)
        db.session.commit()
        flash(_('You have successfully deleted the experiment!'), 'success')
        return redirect(url_for('queries.experiments'))
    except IntegrityError:
        db.session.rollback()
        flash(_('You can not delete this project'), 'danger')
        return redirect(url_for('queries.experiment'))

def save_experiment_changes(experiment, form, new=False):
    experiment.eln = form.eln.data
    experiment.title = form.title.data
    experiment.description = form.description.data
    experiment.site = form.site.data
    experiment.building = form.building.data
    experiment.room = form.room.data
    experiment.created_date = form.created_date.data
    experiment.last_modified_date = stringdatetime()
    if new:
        db.session.add(experiment)

@forms.route('/experiments/<string:id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_experiment(id):
    qry = db.session.query(Experiments).filter(Experiments.id==id)
    experiment = qry.first()
    if experiment:
        create_experiment_form = CreateExperiment(formdata=request.form, obj=experiment)
        if request.method == 'POST' and create_experiment_form.validate():
            try:
                save_experiment_changes(experiment, create_experiment_form)
                db.session.commit()
                flash(_('Experiment updated successfully!'), 'success')
                return redirect(url_for('queries.experiments'))
            except IntegrityError:
                db.session.rollback()
                flash(_('You can not update this experiment - This ELN Number is already in use!'), 'danger')
                return render_template('forms/create-experiment.html', create_experiment_form=create_experiment_form)
        return render_template('forms/create-experiment.html', create_experiment_form=create_experiment_form)
    else:
        return 'Error with Experiment #{guid}'.format(guid=id)