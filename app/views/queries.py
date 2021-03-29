from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

from app.models.model import Projects, Experiments, Sketches
from app.util.datatables import Datatables

queries = Blueprint('queries', __name__)


@queries.route('/projects')
def projects():
    return render_template('interface/projects.html')


@queries.route('/load-projects')
def load_projects():
    if request.method == 'GET':
        returnTable = Datatables(request, Projects).output_result()
        return jsonify(returnTable)


@queries.route('/experiments')
def experiments():
    return render_template('interface/experiments.html')


@queries.route('/load-experiments')
def load_experiments():
    if request.method == 'GET':
        returnTable = Datatables(request, Experiments).output_result()
        return jsonify(returnTable)


@queries.route('/sketches')
def sketches():
    return render_template('interface/sketches.html')


@queries.route('/load-sketches')
def load_sketches():
    if request.method == 'GET':
        returnTable = Datatables(request, Sketches).output_result()
        return jsonify(returnTable)


@queries.route('/choose-project')
@login_required
def choose_projects():
    return render_template('interface/choose-project.html')


@queries.route('/select-project')
@login_required
def load_existing_projects():
    if request.method == 'GET':
        returnTable = Datatables(request, Projects).output_result()
        return jsonify(returnTable)

@queries.route('/choose-experiment')
@login_required
def choose_experiments():
    return render_template('interface/choose-experiment.html')


@queries.route('/select-experiment')
@login_required
def load_existing_experiments():
    if request.method == 'GET':
        returnTable = Datatables(request, Experiments).output_result()
        return jsonify(returnTable)
