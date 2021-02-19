from flask import Blueprint, render_template, request, redirect, url_for, jsonify

from ..util.table_queries import DataTable

queries = Blueprint("queries", __name__)

@queries.route('/projects')
def projects():
    return render_template('projects.html')

@queries.route('/load')
def loadProjects():
    if request.method == 'GET':
        ret = DataTable(request, Projects).output_result()
        return jsonify(ret)

@queries.route('/experiments')
def experiments():
    return render_template('experiments.html')