from flask_login import UserMixin
from . import db
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


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
    experiments = relationship("Experiments", back_populates="sketches")

    def __init__(self, guid, title, user_id, created_date, modified_date):
        self.guid = guid
        self.title = title
        self.user_id = user_id
        self.created_date = created_date
        self.modified_date = modified_date
        
        
class Experiments(db.Model):
    __tablename__ = 'experiments'
    guid = Column(String(200),unique=True, primary_key=True)
    sketch_guid = Column(String(200), db.ForeignKey('sketches.guid'), nullable=False)
    title = Column(String(100), unique=False, nullable=False)
    user_id = Column(Integer, unique=True, nullable=False)
    created_date = Column(Integer, unique=False, nullable=False)
    modified_date = Column(Integer, unique=False, nullable=False)
    sketches = relationship("Sketches", uselist=False, back_populates="experiments")

    def __init__(self, guid, sketch_guid, title, user_id, created_date, modified_date):
        self.guid = guid
        self.sketch_guid = sketch_guid
        self.title = title
        self.user_id = user_id
        self.created_date = created_date
        self.modified_date = modified_date
        
        
class Projects(db.Model):
    __tablename__ = 'projects'
    guid = Column(String(200),unique=True, primary_key=True)
    experiments_guid = Column(db.String(200), db.ForeignKey('experiments.guid'), nullable=False)
    title = Column(String(100), unique=False, nullable=False)
    description = Column(String(1000), unique=False, nullable=False)

    def __init__(self, guid, experiments_guid, title, description):
        self.guid = guid
        self.experiments_guid = experiments_guid
        self.title = title
        self.description = description