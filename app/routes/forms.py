from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from ..models import User, Projects
from .. import db

from sqlalchemy.exc import IntegrityError

forms = Blueprint("forms", __name__)

@forms.route("/create-project", methods=["GET", "POST"])
def create_project():
    from ..form_validation import CreateProject, stringdate

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
                    "Error in {}: {}".format(
                        getattr(create_project_form, field).label.text, error
                    ),
                    "error",
                )
        return render_template(
            "forms/create-project.html", create_project_form=create_project_form
        )
