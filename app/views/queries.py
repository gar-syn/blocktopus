from flask import Blueprint, render_template, request, redirect, url_for, jsonify

from .. import db
from ..models import Projects, Experiments
from ..util.table_queries import ProjectsDataTable, ExperimentsDataTable, ProjectsDataTableToChooseFrom


queries = Blueprint("queries", __name__)

@queries.route('/projects')
def projects():
    return render_template('interface/projects.html')

@queries.route('/load-projects')
def load_projects():
    if request.method == 'GET':
        returnTable = ProjectsDataTable(request, Projects).output_result()
        return jsonify(returnTable)

@queries.route('/experiments')
def experiments():
    return render_template('interface/experiments.html')

@queries.route('/load-experiments')
def load_experiments():
    if request.method == 'GET':
        returnTable = ExperimentsDataTable(request, Experiments).output_result()
        return jsonify(returnTable)
    
@queries.route('/choose-project')
def choose_projects():
    return render_template('interface/choose-project.html')

@queries.route('/select-project')
def load_existing_projects():
    if request.method == 'GET':
        returnTable = ProjectsDataTableToChooseFrom(request, Projects).output_result()
        return jsonify(returnTable)