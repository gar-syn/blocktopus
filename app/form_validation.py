from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField, PasswordField
from wtforms.validators import InputRequired, Length, Regexp, NumberRange

class CreateProject(FlaskForm):
    guid = HiddenField()
    title = StringField('Project Title', [ InputRequired(),
        Regexp(r'^[A-ZÀ-ȕa-z0-9 ]*$', message="Invalid Project Title"),
        Length(min=3, max=75, message="Invalid Project Title length")
        ])
    description = StringField('Project Description', [ InputRequired(),
        Regexp(r'^[A-Za-zÀ-ȕ0-9(),-. ]*$', message="Invalid Project Description"),
        Length(min=1, max=500, message="Invalid Project Description length")
        ])
    created_date = HiddenField()
    submit = SubmitField('Create new Project')
    
class CreateExperiment(FlaskForm):
    select_project_guid = HiddenField()
    guid = HiddenField()
    eln = StringField('Experiment ELN Number', [ InputRequired(),
        Regexp(r'[A-Za-z0-9 ]*$', message="Invalid ELN"),
        Length(min=1, max=40, message="Invalid ELN length")
        ])    
    title = StringField('Experiment Title', [ InputRequired(),
        Regexp(r'^[A-ZÀ-ȕa-z0-9 ]*$', message="Invalid Experiment Title"),
        Length(min=3, max=75, message="Invalid Experiment Title length")
        ])
    description = StringField('Experiment Description', [ InputRequired(),
        Regexp(r'^[A-Za-zÀ-ȕ0-9(),-. ]*$', message="Invalid Experiment Description"),
        Length(min=1, max=500, message="Invalid Experiment Description length")
        ])
    site = StringField('Site', [ InputRequired(),
        Regexp(r'^[A-ZÀ-ȕa-z0-9 /]*$', message="Invalid Experiment Site"),
        Length(min=1, max=75, message="Invalid Experiment Site length")
        ])
    building = StringField('Building', [ InputRequired(),
        Regexp(r'^[A-ZÀ-ȕa-z0-9 /]*$', message="Invalid Experiment Building"),
        Length(min=1, max=75, message="Invalid Experiment Building length")
        ])
    room = StringField('Room', [ InputRequired(),
        Regexp(r'^[A-Za-z0-9 /]*$', message="Invalid Experiment Room"),
        Length(min=1, max=75, message="Invalid Experiment Room length")
        ])
    user_id = HiddenField()
    created_date = HiddenField()
    last_modified_date = HiddenField()
    submit = SubmitField('Create new Experiment')
    
class ChangeSite(FlaskForm):
    site = StringField('Site', [ InputRequired(),
        Regexp(r'^[A-ZÀ-ȕa-z0-9 /]*$', message="Invalid Experiment Site"),
        Length(min=1, max=75, message="Invalid Experiment Site length")
        ])
    submit = SubmitField('Change your site')

class ChangeBuilding(FlaskForm):
    building = StringField('Building', [ InputRequired(),
        Regexp(r'^[A-ZÀ-ȕa-z0-9 /]*$', message="Invalid Experiment Building"),
        Length(min=1, max=75, message="Invalid Experiment Building length")
        ])
    submit = SubmitField('Change your building')

class ChangeRoom(FlaskForm):
    room = StringField('Room', [ InputRequired(),
        Regexp(r'^[A-Za-z0-9 /]*$', message="Invalid Experiment Room"),
        Length(min=1, max=75, message="Invalid Experiment Room length")
        ])
    submit = SubmitField('Change your room')

class ChangePassword(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Change your password')