from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField
from wtforms.validators import InputRequired, Length, Regexp, NumberRange
from datetime import date

class CreateProject(FlaskForm):
    guid = StringField('Project GUID', [ InputRequired(),
        Regexp(r'[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}', message="Invalid GUID"),
        Length(min=36, max=36, message="Invalid GUID length")
        ])
    title = StringField('Project Title', [ InputRequired(),
        Regexp(r'^[A-Za-z0-9 ]*$', message="Invalid Project Title"),
        Length(min=3, max=75, message="Invalid Project Title length")
        ])
    description = StringField('Project Description', [ InputRequired(),
        Regexp(r'^[A-Za-z0-9 .]*$', message="Invalid Project Description"),
        Length(min=1, max=500, message="Invalid Project Description length")
        ])
    created_date = HiddenField()
    submit = SubmitField('Create new Project')
    
class CreateExperiment(FlaskForm):
    guid = StringField('Experiment GUID', [ InputRequired(),
        Regexp(r'[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}', message="Invalid GUID"),
        Length(min=36, max=36, message="Invalid GUID length")
        ])
    eln = StringField('Experiment ELN Number', [ InputRequired(),
        Regexp(r'[A-Za-z0-9 ]*$', message="Invalid ELN"),
        Length(min=1, max=40, message="Invalid ELN length")
        ])    
    title = StringField('Experiment Title', [ InputRequired(),
        Regexp(r'^[A-Za-z0-9 ]*$', message="Invalid Experiment Title"),
        Length(min=3, max=75, message="Invalid Experiment Title length")
        ])
    description = StringField('Experiment Description', [ InputRequired(),
        Regexp(r'^[A-Za-z0-9 .]*$', message="Invalid Experiment Description"),
        Length(min=1, max=500, message="Invalid Experiment Description length")
        ])
    site = StringField('Site', [ InputRequired(),
        Regexp(r'^[A-Za-z0-9 ]*$', message="Invalid Experiment Site"),
        Length(min=1, max=75, message="Invalid Experiment Site length")
        ])
    building = StringField('Building', [ InputRequired(),
        Regexp(r'^[A-Za-z0-9 ]*$', message="Invalid Experiment Building"),
        Length(min=1, max=75, message="Invalid Experiment Building length")
        ])
    room = StringField('Room', [ InputRequired(),
        Regexp(r'^[A-Za-z0-9 ]*$', message="Invalid Experiment Room"),
        Length(min=1, max=75, message="Invalid Experiment Room length")
        ])
    user_id = HiddenField()
    created_date = HiddenField()
    last_modified_date = HiddenField()
    submit = SubmitField('Create new Experiment')

def stringdate():
    today = date.today()
    date_list = str(today).split('-')
    date_string = date_list[2] + "." + date_list[1] + "." + date_list[0]
    return date_string