import os
import sys
import unittest

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

if __name__ == '__main__':
    manager.run()