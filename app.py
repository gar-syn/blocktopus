import os
import sys
import unittest
import pytest

from app import create_app
from app.util.extensions import db, babel
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import request, session

base_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__name__))

app = create_app('dev')
app.config["BABEL_TRANSLATION_DIRECTORIES"] = os.path.join(base_dir, "app/static/translations")
app.app_context().push()
db.create_all()

@babel.localeselector
def get_locale():
    try:
        language = session['language']
    except KeyError:
        language = None
    if language is not None:
        return language
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())

@app.context_processor
def inject_conf_var():
    return dict(AVAILABLE_LANGUAGES=app.config['LANGUAGES'],
                CURRENT_LANGUAGE=session.get('language',request.accept_languages.best_match(app.config['LANGUAGES'].keys())))


manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run()

@manager.command
def test():
    """Runs the pytest unit tests."""
    print("Running unit tests...")
    pytest.main(['--rootdir', './app/tests/unit/'])
    """Runs the nose2 functional tests."""
    print("Running functional tests...")
    tests = unittest.TestLoader().discover('app/tests/functional/', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()