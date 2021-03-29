from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.util.sqltypes import generate_uuid
from app.util.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = Column(String(36), unique=True, primary_key=True, default=generate_uuid)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), unique=False, nullable=False)
    name = Column(String(32), unique=False, nullable=False)
    site = Column(String(16), unique=False)
    building = Column(String(16), unique=False)
    room = Column(String(16), unique=False)

    def __init__(self, email, password, name, site, building, room):
        self.email = email
        self.password = password
        self.name = name
        self.site = site
        self.building = building
        self.room = room

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {0}>'.format(self.name)


class Sketches(db.Model):
    __tablename__ = 'sketches'
    id = Column(String(36), unique=True, primary_key=True, default=generate_uuid)
    title = Column(String(32), unique=False, nullable=False)
    user_id = Column(String(36), unique=False)
    created_date = Column(Integer, unique=False, nullable=False)
    modified_date = Column(Integer, unique=False, nullable=False)
    experiment_id = Column(String(36), ForeignKey('experiments.id'), nullable=False, unique=True)
    experiments = relationship("Experiments", back_populates="sketches")

    def __init__(self, title, user_id, created_date, modified_date, experiment_id):
        self.title = title
        self.user_id = user_id
        self.created_date = created_date
        self.modified_date = modified_date
        self.experiment_id = experiment_id

    @property
    def table_to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'user_id': self.user_id,
            'created_date': self.created_date,
            'modified_date': self.modified_date,
            'experiment_id': self.experiment_id,
        }


class Experiments(db.Model):
    __tablename__ = 'experiments'
    id = Column(String(36), unique=True, primary_key=True, default=generate_uuid)
    eln = Column(String(36), unique=True)
    title = Column(String(64), unique=False, nullable=False)
    description = Column(String(256), unique=False, nullable=False)
    site = Column(String(32), unique=False)
    building = Column(String(32), unique=False)
    room = Column(String(32), unique=False)
    user_id = Column(String(36), unique=False)
    created_date = Column(Integer, unique=False, nullable=False)
    last_modified_date = Column(Integer, unique=False)
    project_id = Column(String(36), ForeignKey('projects.id'), nullable=False)
    sketches = relationship("Sketches", uselist=False, back_populates="experiments")

    def __init__(self, eln, title, description, site, building, room, user_id, created_date, last_modified_date, project_id):
        self.eln = eln
        self.title = title
        self.description = description
        self.site = site
        self.building = building
        self.room = room
        self.user_id = user_id
        self.created_date = created_date
        self.last_modified_date = last_modified_date
        self.project_id = project_id

    @property
    def table_to_json(self):
        return {
            'id': self.id,
            'eln': self.eln,
            'title': self.title,
            'description': self.description,
            'site': self.site,
            'building': self.building,
            'room': self.room,
            'user_id': self.user_id,
            'created_date': self.created_date,
            'last_modified_date': self.last_modified_date,
            'project_id': self.project_id,
        }


class Projects(db.Model):
    __tablename__ = 'projects'
    id = Column(String(36), unique=True, primary_key=True, default=generate_uuid)
    title = Column(String(64), unique=False, nullable=False)
    description = Column(String(256), unique=False, nullable=False)
    created_date = Column(Integer, unique=False, nullable=False)
    experiments = relationship("Experiments", backref='projects', lazy=True)

    def __init__(self, title, description, created_date):
        self.title = title
        self.description = description
        self.created_date = created_date

    @property
    def table_to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_date': self.created_date,
        }
