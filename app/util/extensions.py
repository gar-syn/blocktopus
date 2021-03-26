from flask_sqlalchemy import SQLAlchemy
from flask_jsglue import JSGlue
from celery import Celery
from flask_bootstrap import Bootstrap
from flask_babel import Babel
from flask_migrate import Migrate
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension

toolbar = DebugToolbarExtension()
babel = Babel()
db = SQLAlchemy()
jsglue = JSGlue()
bootstrap = Bootstrap()
migrate = Migrate()
cache = Cache()


def create_celery_app(app=None):
    app = app or create_app()
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):

        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    celery.app = app
    return celery
