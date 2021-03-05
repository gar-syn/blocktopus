from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean, Binary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from flask import Markup
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from ..util.extensions import db, bcrypt

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), unique=False, nullable=False)
    name = Column(String(100), unique=False, nullable=False)
    site = Column(String(100), unique=False)
    building = Column(String(100), unique=False)
    room = Column(String(100), unique=False)

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
    guid = Column(String(200),unique=True, primary_key=True)
    title = Column(String(100), unique=False, nullable=False)
    user_id = Column(Integer, unique=True, nullable=False)
    created_date = Column(Integer, unique=False, nullable=False)
    modified_date = Column(Integer, unique=False, nullable=False)
    #experiments = relationship("Experiments", back_populates="sketches")

    def __init__(self, guid, title, user_id, created_date, modified_date):
        self.guid = guid
        self.title = title
        self.user_id = user_id
        self.created_date = created_date
        self.modified_date = modified_date
        
class Experiments(db.Model):
    __tablename__ = 'experiments'
    guid = Column(String(200),unique=True, primary_key=True)
    eln = Column(String(100), unique=True)
    title = Column(String(100), unique=False, nullable=False)
    description = Column(String(500), unique=False, nullable=False)
    site = Column(String(50), unique=False)
    building = Column(String(30), unique=False)
    room = Column(String(30), unique=False)
    user_id = Column(Integer, unique=False)
    created_date = Column(Integer, unique=False, nullable=False)
    last_modified_date = Column(Integer, unique=False)
    project_guid = Column(String, ForeignKey('projects.guid'), nullable=False)
    #sketch_guid = Column(String(200), ForeignKey('sketches.guid'), nullable=False)
    #sketches = relationship("Sketches", uselist=False, back_populates="experiments")

    def __init__(self, guid, eln, title, description, site, building, room, user_id, created_date, last_modified_date, project_guid):
        self.guid = guid
        self.eln = eln
        self.title = title
        self.description = description
        self.site = site
        self.building = building
        self.room = room
        self.user_id = user_id
        self.created_date = created_date
        self.last_modified_date = last_modified_date
        self.project_guid = project_guid
        
    def __repr__(self):
        return '<Project GUID {}>'.format(self.project_guid)

    @property
    def experiments_table_to_json(self):
        return {
            'guid': self.guid,
            'eln': self.eln,
            'title': self.title,
            'description': self.description,
            'site': self.site,
            'building': self.building,
            'room': self.room,
            'description': self.description,
            'user_id': self.user_id,
            'created_date': self.created_date,
            'last_modified_date': self.last_modified_date,
            'project_guid': self.project_guid,
        }
        
class Projects(db.Model):
    __tablename__ = 'projects'
    guid = Column(String(200),unique=True, primary_key=True)
    title = Column(String(100), unique=False, nullable=False)
    description = Column(String(500), unique=False, nullable=False)
    created_date = Column(Integer, unique=False, nullable=False)
    experiments = relationship("Experiments", backref='project', lazy=True)

    def __init__(self, guid, title, description, created_date):
        self.guid = guid
        self.title = title
        self.description = description
        self.created_date = created_date
        
    def __repr__(self):
        return '<Project {}>'.format(self.title)
    
    @property
    def projects_table_to_json(self):
        return {
            'guid': self.guid,
            'title': self.title,
            'description': self.description,
            'created_date': self.created_date,
        }