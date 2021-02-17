from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'flasklogin-users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)
    name = db.Column(db.String(100), unique=False, nullable=False)

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.name
    

class Sketches(db.Model):
    __tablename__ = 'sketches'
    guid = db.Column(db.String(200),unique=True, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    created_date = db.Column(db.Integer, unique=False, nullable=False)
    modified_date = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, guid, title, user_id, created_date, modified_date):
        self.guid = guid
        self.title = title
        self.user_id = user_id
        self.created_date = created_date
        self.modified_date = modified_date
        
        
class Experiments(db.Model):
    __tablename__ = 'experiments'
    guid = db.Column(db.String(200),unique=True, primary_key=True)
    sketch_guid = db.Column(db.String(200), db.ForeignKey('sketches.guid'), nullable=False)
    title = db.Column(db.String(100), unique=False, nullable=False)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    created_date = db.Column(db.Integer, unique=False, nullable=False)
    modified_date = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, guid, sketch_guid, title, user_id, created_date, modified_date):
        self.guid = guid
        self.sketch_guid = sketch_guid
        self.title = title
        self.user_id = user_id
        self.created_date = created_date
        self.modified_date = modified_date
        
        
class Projects(db.Model):
    __tablename__ = 'projects'
    guid = db.Column(db.String(200),unique=True, primary_key=True)
    experiments_guid = db.Column(db.String(200), db.ForeignKey('experiments.guid'), nullable=False)
    title = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.String(1000), unique=False, nullable=False)

    def __init__(self, guid, experiments_guid, title, description):
        self.guid = guid
        self.experiments_guid = experiments_guid
        self.title = title
        self.description = description