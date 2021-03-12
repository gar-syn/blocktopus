from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, Regexp, NumberRange, EqualTo
from wtforms.fields.html5 import EmailField
from flask_babel import lazy_gettext as _l

class RegisterForm(FlaskForm):
    email = EmailField(_l('Email'), validators=[InputRequired(), Length(min=6, max=40)])
    password = PasswordField(_l('Password'), validators=[InputRequired(), Length(min=3, max=40)])
    confirm = PasswordField(_l('Repeat Password'), validators=[InputRequired(), EqualTo('password')])
    name = StringField(_l('Name'), [ InputRequired(),
        Regexp(r'^[A-Za-zÀ-ȕ0-9(),-. ]*$', message="Invalid Experiment Description"),
        Length(min=1, max=500, message="Invalid Experiment Description length")
        ])
    site = StringField(_l('Site'), [ InputRequired(),
        Regexp(r'^[A-ZÀ-ȕa-z0-9 /]*$', message="Invalid Experiment Site"),
        Length(min=1, max=75, message="Invalid Experiment Site length")
        ])
    building = StringField(_l('Building'), [ InputRequired(),
        Regexp(r'^[A-ZÀ-ȕa-z0-9 /]*$', message="Invalid Experiment Building"),
        Length(min=1, max=75, message="Invalid Experiment Building length")
        ])
    room = StringField(_l('Room'), [ InputRequired(),
        Regexp(r'^[A-Za-z0-9 /]*$', message="Invalid Experiment Room"),
        Length(min=1, max=75, message="Invalid Experiment Room length")
        ])
    submit = SubmitField('')

class LoginForm(FlaskForm):
    email = EmailField(_l('Email'), validators=[InputRequired()])
    password = PasswordField(_l('Password'), validators=[InputRequired()])
    remember_me = BooleanField(_l('Remember Me'))

class CreateProject(FlaskForm):
    title = StringField(_l('Title'), [ InputRequired(),
        Regexp(r'^[A-ZÀ-ȕa-z0-9 ]*$', message="Invalid Project Title"),
        Length(min=3, max=75, message="Invalid Project Title length")
        ])
    description = TextAreaField(_l('Description'), [ InputRequired(),
        Regexp(r'^[A-Za-zÀ-ȕ0-9(),-. ]*$', message="Invalid Project Description"),
        Length(min=1, max=500, message="Invalid Project Description length")
        ])
    created_date = HiddenField()
    submit = SubmitField(_l('Create new Project'))
    
class CreateExperiment(FlaskForm):
    select_project_id = HiddenField()
    eln = StringField(_l('Experiment ELN Number'), [ InputRequired(),
        Regexp(r'[A-Za-z0-9 ]*$', message="Invalid ELN"),
        Length(min=1, max=40, message="Invalid ELN length")
        ])    
    title = StringField(_l('Experiment Title'), [ InputRequired(),
        Regexp(r'^[A-ZÀ-ȕa-z0-9 ]*$', message="Invalid Experiment Title"),
        Length(min=3, max=75, message="Invalid Experiment Title length")
        ])
    description = TextAreaField(_l('Experiment Description'), [ InputRequired(),
        Regexp(r'^[A-Za-zÀ-ȕ0-9(),-. ]*$', message="Invalid Experiment Description"),
        Length(min=1, max=500, message="Invalid Experiment Description length")
        ])
    site = StringField(_l('Site'), [ InputRequired(),
        Regexp(r'^[A-ZÀ-ȕa-z0-9 /]*$', message="Invalid Experiment Site"),
        Length(min=1, max=75, message="Invalid Experiment Site length")
        ])
    building = StringField(_l('Building'), [ InputRequired(),
        Regexp(r'^[A-ZÀ-ȕa-z0-9 /]*$', message="Invalid Experiment Building"),
        Length(min=1, max=75, message="Invalid Experiment Building length")
        ])
    room = StringField(_l('Room'), [ InputRequired(),
        Regexp(r'^[A-Za-z0-9 /]*$', message="Invalid Experiment Room"),
        Length(min=1, max=75, message="Invalid Experiment Room length")
        ])
    user_id = HiddenField()
    created_date = HiddenField()
    last_modified_date = HiddenField()
    submit = SubmitField(_l('Create new Experiment'))
    
class ChangeSite(FlaskForm):
    site = StringField(_l('Site'), [ InputRequired(),
        Regexp(r'^[A-ZÀ-ȕa-z0-9 /]*$', message="Invalid Experiment Site"),
        Length(min=1, max=75, message="Invalid Experiment Site length")
        ])
    submit = SubmitField(_l('Change your site'))

class ChangeBuilding(FlaskForm):
    building = StringField(_l('Building'), [ InputRequired(),
        Regexp(r'^[A-ZÀ-ȕa-z0-9 /]*$', message="Invalid Experiment Building"),
        Length(min=1, max=75, message="Invalid Experiment Building length")
        ])
    submit = SubmitField(_l('Change your building'))

class ChangeRoom(FlaskForm):
    room = StringField(_l('Room'), [ InputRequired(),
        Regexp(r'^[A-Za-z0-9 /]*$', message="Invalid Experiment Room"),
        Length(min=1, max=75, message="Invalid Experiment Room length")
        ])
    submit = SubmitField(_l('Change your room'))
    
class ChangeEmail(FlaskForm):
    email = EmailField(_l('Email'), validators=[InputRequired()])
    submit = SubmitField(_l('Change your Email'))
    
class ChangePassword(FlaskForm):
    password = PasswordField(_l('Your new Password'), validators=[InputRequired()],id='password')
    show_password = BooleanField(_l('Show password'), id='check')
    submit = SubmitField(_l('Change your password'))