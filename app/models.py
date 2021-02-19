from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), unique=False, nullable=False)
    name = Column(String(100), unique=False, nullable=False)

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.name
    
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
    eln = Column(String(100))
    title = Column(String(100), unique=False, nullable=False)
    description = Column(String(500), unique=False, nullable=False)
    site = Column(String(50), unique=False)
    building = Column(String(30), unique=False)
    room = Column(String(30), unique=False)
    user_id = Column(Integer, unique=False)
    created_date = Column(Integer, unique=False, nullable=False)
    last_modified_date = Column(Integer, unique=False)
    project_guid = Column(String, ForeignKey('projects.guid'))
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
        return unicode(self.guid)
    
    @property
    def projects_table_to_json(self):
        return {
            'guid': self.guid,
            'title': self.title,
            'description': self.description,
            'created_date': self.created_date,
        }