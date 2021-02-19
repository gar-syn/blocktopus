from flask import Blueprint, render_template, request, redirect, url_for, jsonify

from .. import db
from ..models import Projects, Experiments
from ..util.table_queries import ProjectsDataTable, ExperimentsDataTable


queries = Blueprint("queries", __name__)

@queries.route('/projects')
def projects():
    return render_template('projects.html')

@queries.route('/load-projects')
def loadProjects():
    if request.method == 'GET':
        ret = ProjectsDataTable(request, Projects).output_result()
        return jsonify(ret)

@queries.route('/experiments')
def experiments():
    return render_template('experiments.html')

@queries.route('/load-experiments')
def loadExperiments():
    if request.method == 'GET':
        ret = ExperimentsDataTable(request, Experiments).output_result()
        return jsonify(ret)