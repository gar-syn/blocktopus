from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, \
    StringField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, Regexp, EqualTo
from wtforms.fields.html5 import EmailField
from flask_babel import lazy_gettext as _l


class RegisterForm(FlaskForm):

    email = EmailField(_l('Email'), validators=[InputRequired(),
                    Length(min=6, max=40)],
                    render_kw={'placeholder': _l('Email')})
    password = PasswordField(_l('Password'),
                    validators=[InputRequired(),
                    Length(min=3, max=40)],
                    render_kw={'placeholder': _l('Password')})
    confirm = PasswordField(_l('Repeat Password'),
                    validators=[InputRequired(),
                    EqualTo('password')],
                    render_kw={'placeholder': _l('Confirm your password')})
    name = StringField(_l('Name'), [InputRequired(),
                    Regexp('^[A-Za-z\xc3\x80-\xc8\x950-9(),-. ]*$',
                    message=_l('Invalid Experiment Description')),
                    Length(min=1, max=50,
                    message=_l('Invalid Experiment Description length'))],
                    render_kw={'placeholder': _l('Name')})
    site = StringField(_l('Site'), [InputRequired(),
                    Regexp('^[A-Z\xc3\x80-\xc8\x95a-z0-9 /]*$',
                    message=_l('Invalid Experiment Site')),
                    Length(min=1, max=32,
                    message=_l('Invalid Experiment Site length'))],
                    render_kw={'placeholder': _l('Site')})
    building = StringField(_l('Building'), [InputRequired(),
                    Regexp('^[A-Z\xc3\x80-\xc8\x95a-z0-9 /]*$',
                    message=_l('Invalid Experiment Building')),
                    Length(min=1, max=32,
                    message=_l('Invalid Experiment Building length'))],
                    render_kw={'placeholder': _l('Building')})
    room = StringField(_l('Room'), [InputRequired(),
                    Regexp(r'^[A-Za-z0-9 /]*$',
                    message=_l('Invalid Experiment Room')),
                    Length(min=1, max=32,
                    message=_l('Invalid Experiment Room length'))],
                    render_kw={'placeholder': _l('Room')})
    submit = SubmitField('')


class LoginForm(FlaskForm):

    email = EmailField(_l('Email'), validators=[InputRequired()],
                    render_kw={'placeholder': _l('Email')})
    password = PasswordField(_l('Password'),
                    validators=[InputRequired()],
                    render_kw={'placeholder': _l('Password')})
    remember_me = BooleanField(_l('Remember Me'))


class CreateProject(FlaskForm):

    title = StringField(_l('Title'), [InputRequired(),
                    Regexp('^[A-Z\xc3\x80-\xc8\x95a-z0-9 ]*$',
                    message=_l('Invalid Project Title')),
                    Length(min=3, max=64,
                    message=_l('Invalid Project Title length'))],
                    render_kw={'placeholder': _l('Title')})
    description = TextAreaField(_l('Description'), [InputRequired(),
                    Regexp('^[A-Za-z\xc3\x80-\xc8\x950-9(),-. ]*$',
                    message=_l('Invalid Project Description')),
                    Length(min=1, max=256,
                    message=_l('Invalid Project Description length'))],
                    render_kw={'placeholder': _l('Description')})
    created_date = HiddenField()
    submit = SubmitField(_l('Create new Project'))


class CreateExperiment(FlaskForm):

    select_project_id = HiddenField()
    eln = StringField(_l('Experiment ELN Number'), [InputRequired(),
                    Regexp(r'[A-Za-z0-9 ]*$',
                    message=_l('Invalid ELN')),
                    Length(min=1, max=40,
                    message=_l('Invalid ELN length'))],
                    render_kw={'placeholder': _l('ELN')})
    title = StringField(_l('Experiment Title'), [InputRequired(),
                    Regexp('^[A-Z\xc3\x80-\xc8\x95a-z0-9 ]*$',
                    message=_l('Invalid Experiment Title')),
                    Length(min=3, max=64,
                    message=_l('Invalid Experiment Title length'
                    ))], render_kw={'placeholder': _l('Title')})
    description = TextAreaField(_l('Experiment Description'),
                    [InputRequired(),
                    Regexp('^[A-Za-z\xc3\x80-\xc8\x950-9(),-. ]*$',
                    message=_l('Invalid Experiment Description')),
                    Length(min=1, max=256,
                    message=_l('Invalid Experiment Description length'))],
                    render_kw={'placeholder': _l('Description')})
    site = StringField(_l('Site'), [InputRequired(),
                    Regexp('^[A-Z\xc3\x80-\xc8\x95a-z0-9 /]*$',
                    message=_l('Invalid Experiment Site')),
                    Length(min=1, max=32,
                    message=_l('Invalid Experiment Site length'))],
                    render_kw={'placeholder': _l('Site')})
    building = StringField(_l('Building'), [InputRequired(),
                    Regexp('^[A-Z\xc3\x80-\xc8\x95a-z0-9 /]*$',
                    message=_l('Invalid Experiment Building')),
                    Length(min=1, max=32,
                    message=_l('Invalid Experiment Building length'))],
                    render_kw={'placeholder': _l('Building')})
    room = StringField(_l('Room'), [InputRequired(),
                    Regexp(r'^[A-Za-z0-9 /]*$',
                    message=_l('Invalid Experiment Room')),
                    Length(min=1, max=32,
                    message=_l('Invalid Experiment Room length'))],
                    render_kw={'placeholder': _l('Room')})
    user_id = HiddenField()
    created_date = HiddenField()
    last_modified_date = HiddenField()
    submit = SubmitField(_l('Create new Experiment'))


class CreateSketch(FlaskForm):
    
    title = StringField(_l('Title'), [InputRequired(),
                    Regexp('^[A-Z\xc3\x80-\xc8\x95a-z0-9 ]*$',
                    message=_l('Invalid Project Title')),
                    Length(min=3, max=64,
                    message=_l('Invalid Project Title length'))],
                    render_kw={'placeholder': _l('Title')})
    created_date = HiddenField()
    last_modified_date = HiddenField()
    select_experiment_guid = HiddenField()
    submit = SubmitField(_l('Create new Sketch'))


class ChangeSite(FlaskForm):

    site = StringField(_l('Site'), [InputRequired(),
                    Regexp('^[A-Z\xc3\x80-\xc8\x95a-z0-9 /]*$',
                    message=_l('Invalid Experiment Site')),
                    Length(min=1, max=32,
                    message=_l('Invalid Experiment Site length'))],
                    render_kw={'placeholder': _l('Site')})
    submit = SubmitField(_l('Change your site'))


class ChangeBuilding(FlaskForm):

    building = StringField(_l('Building'), [InputRequired(),
                    Regexp('^[A-Z\xc3\x80-\xc8\x95a-z0-9 /]*$',
                    message=_l('Invalid Experiment Building')),
                    Length(min=1, max=32,
                    message=_l('Invalid Experiment Building length'))],
                    render_kw={'placeholder': _l('Building')})
    submit = SubmitField(_l('Change your building'))


class ChangeRoom(FlaskForm):

    room = StringField(_l('Room'), [InputRequired(),
                    Regexp(r'^[A-Za-z0-9 /]*$',
                    message=_l('Invalid Experiment Room')),
                    Length(min=1, max=32,
                    message=_l('Invalid Experiment Room length'))],
                    render_kw={'placeholder': _l('Room')})
    submit = SubmitField(_l('Change your room'))


class ChangeEmail(FlaskForm):

    email = EmailField(_l('Email'), validators=[InputRequired()],
                    render_kw={'placeholder': _l('Email')})
    submit = SubmitField(_l('Change your Email'))


class ChangePassword(FlaskForm):

    password = PasswordField(_l('Your new Password'),
                    validators=[InputRequired()], id='password',
                    render_kw={'placeholder': _l('Password')})
    show_password = BooleanField(_l('Show password'), id='check')
    submit = SubmitField(_l('Change your password'))
