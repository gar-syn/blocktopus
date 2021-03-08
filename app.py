import os
import sys
import unittest
import pytest

from app import create_app
from app.util.extensions import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

sys.path.append(os.path.dirname(__name__))

app = create_app()
app.app_context().push()
db.create_all()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run()

@manager.command
def test():
    """Runs the pytest unit tests."""
    print("Running unit tests")
    pytest.main(['--rootdir', './app/tests/unit/'])
    """Runs the nose2 functional tests."""
    print("Running functional tests")
    tests = unittest.TestLoader().discover('app/tests/functional/', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()