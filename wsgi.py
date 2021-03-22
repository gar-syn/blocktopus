#Fask Entrypoint
from app import create_app
from app.util.extensions import db, migrate
from app.util.logging import initialize_flask_logger
from flask_script import Manager
from flask_migrate import MigrateCommand

app = create_app('dev')
app.app_context().push()
db.create_all()
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    initialize_flask_logger(app)
    app.run()