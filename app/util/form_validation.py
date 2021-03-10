from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, Regexp, NumberRange, EqualTo
from wtforms.fields.html5 import EmailField

class RegisterForm(FlaskForm):
    email = EmailField('', validators=[InputRequired(), Length(min=6, max=40)], render_kw={"placeholder": "Your Email",})
    password = PasswordField('', validators=[InputRequired(), Length(min=3, max=40)])
    #confirm = PasswordField('Repeat Password', validators=[InputRequired(), EqualTo('password')])
    name = StringField('', [ InputRequired(),
        Regexp(r'^[A-Za-zÀ-ȕ0-9(),-. ]*$', message="Invalid Experiment Description"),
        Length(min=1, max=500, message="Invalid Experiment Description length")
        ], render_kw={"placeholder": "Your name",})
    site = StringField('', [ InputRequired(),
        Regexp(r'^[A-ZÀ-ȕa-z0-9 /]*$', message="Invalid Experiment Site"),
        Length(min=1, max=75, message="Invalid Experiment Site length")
        ])
    building = StringField('', [ InputRequired(),
        Regexp(r'^[A-ZÀ-ȕa-z0-9 /]*$', message="Invalid Experiment Building"),
        Length(min=1, max=75, message="Invalid Experiment Building length")
        ])
    room = StringField('', [ InputRequired(),
        Regexp(r'^[A-Za-z0-9 /]*$', message="Invalid Experiment Room"),
        Length(min=1, max=75, message="Invalid Experiment Room length")
        ])
    submit = SubmitField('')

class LoginForm(FlaskForm):
    email = EmailField('', validators=[InputRequired()])
    password = PasswordField('', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')

class CreateProject(FlaskForm):
    title = StringField('', [ InputRequired(),
        Regexp(r'^[A-ZÀ-ȕa-z0-9 ]*$', message="Invalid Project Title"),
        Length(min=3, max=75, message="Invalid Project Title length")
        ])
    description = TextAreaField('', [ InputRequired(),
        Regexp(r'^[A-Za-zÀ-ȕ0-9(),-. ]*$', message="Invalid Project Description"),
        Length(min=1, max=500, message="Invalid Project Description length")
        ])
    created_date = HiddenField()
    submit = SubmitField('Create new Project')
    
class CreateExperiment(FlaskForm):
    select_project_id = HiddenField()
    eln = StringField('Experiment ELN Number', [ InputRequired(),
        Regexp(r'[A-Za-z0-9 ]*$', message="Invalid ELN"),
        Length(min=1, max=40, message="Invalid ELN length")
        ])    
    title = StringField('Experiment Title', [ InputRequired(),
        Regexp(r'^[A-ZÀ-ȕa-z0-9 ]*$', message="Invalid Experiment Title"),
        Length(min=3, max=75, message="Invalid Experiment Title length")
        ])
    description = TextAreaField('Experiment Description', [ InputRequired(),
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
    
class ChangeEmail(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    submit = SubmitField('Change your Email')
    
class ChangePassword(FlaskForm):
    password = PasswordField('Your new Password', validators=[InputRequired()],id='password')
    show_password = BooleanField('Show password', id='check')
    submit = SubmitField('Change your password')