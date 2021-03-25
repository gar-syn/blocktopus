from flask import request
from sqlalchemy import or_, and_
from sqlalchemy.sql import func

from app.util.extensions import db

#Server Side processing for data tables
class ProjectsDataTable:
    def __init__(self, request, model_object):
        self.request = request
        self.model_object = model_object
        self.cardinality = 0
        self.cardinality_filtered = 0
        self.results = None
        self.run_query()

    def output_result(self):
        output = {}
        output["sEcho"] = int(self.request.args.get('sEcho'))
        output["iTotalRecords"] = self.cardinality
        output["iTotalDisplayRecords"] = self.cardinality_filtered
        output["aaData"] = self.results
        return output

    def run_query(self):
        self.cardinality = db.session.query(func.count(self.model_object.id)).first()
        column_count = int(self.request.args.get('iColumns'))
        column_list = []
        for i in range(column_count):
            column_name = self.request.args.get('mDataProp_%d' % i)
            if column_name:
                column_list.append(column_name)

        #filtering
        search_value = self.request.args.get('sSearch')
        filter_list = []
        if search_value != "":
            for col in column_list:
                column_type = getattr(getattr(self.model_object, col), 'type')
                if not isinstance(column_type, db.DateTime):
                    filter_list.append(getattr(self.model_object, col).like("%" + search_value + "%"))

        #sorting
        order_column_index = int(self.request.args.get('iSortCol_0'))
        order_column = getattr(self.model_object, column_list[order_column_index])
        order_dir = self.request.args.get('sSortDir_0')
        order_object = getattr(order_column, order_dir)()

        #paging
        start = self.request.args.get('iDisplayStart', 0, type=int)
        length = self.request.args.get('iDisplayLength', 1, type=int)

        items = self.model_object.query.filter(or_(*filter_list)).order_by(order_object) \
                    .offset(start).limit(length).all()
        self.cardinality_filtered = db.session.query(func.count(self.model_object.id)) \
                    .filter(or_(*filter_list)).order_by(None).first()
        self.results = [i.projects_table_to_json for i in items]
        
class ExperimentsDataTable:
    def __init__(self, request, model_object):
        self.request = request
        self.model_object = model_object
        self.cardinality = 0
        self.cardinality_filtered = 0
        self.results = None
        self.run_query()

    def output_result(self):
        output = {}
        output["sEcho"] = int(self.request.args.get('sEcho'))
        output["iTotalRecords"] = self.cardinality
        output["iTotalDisplayRecords"] = self.cardinality_filtered
        output["aaData"] = self.results
        return output

    def run_query(self):
        self.cardinality = db.session.query(func.count(self.model_object.id)).first()
        column_count = int(self.request.args.get('iColumns'))
        column_list = []
        for i in range(column_count):
            column_name = self.request.args.get('mDataProp_%d' % i)
            if column_name:
                column_list.append(column_name)

        search_value = self.request.args.get('sSearch')
        filter_list = []
        if search_value != "":
            for col in column_list:
                column_type = getattr(getattr(self.model_object, col), 'type')
                if not isinstance(column_type, db.DateTime):
                    filter_list.append(getattr(self.model_object, col).like("%" + search_value + "%"))

        order_column_index = int(self.request.args.get('iSortCol_0'))
        order_column = getattr(self.model_object, column_list[order_column_index])
        order_dir = self.request.args.get('sSortDir_0')
        order_object = getattr(order_column, order_dir)()

        start = self.request.args.get('iDisplayStart', 0, type=int)
        length = self.request.args.get('iDisplayLength', 1, type=int)

        items = self.model_object.query.filter(or_(*filter_list)).order_by(order_object) \
                    .offset(start).limit(length).all()
        self.cardinality_filtered = db.session.query(func.count(self.model_object.id)) \
                    .filter(or_(*filter_list)).order_by(None).first()
        self.results = [i.experiments_table_to_json for i in items]