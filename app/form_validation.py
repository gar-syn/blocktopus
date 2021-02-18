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
    created = HiddenField()
    submit = SubmitField('Create new Project')

def stringdate():
    today = date.today()
    date_list = str(today).split('-')
    date_string = date_list[1] + "-" + date_list[2] + "-" + date_list[0]
    return date_string
