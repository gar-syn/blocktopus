import os
import sys
from flask import Flask, render_template, session, request
from flask_assets import Environment
from flask_login import LoginManager

from app.util.config import configuration_classes
from app.util.extensions import db, jsglue, bootstrap, create_celery_app, babel

def create_app(config_object='dev'):
    app = Flask(__name__)
    app.config.from_object(configuration_classes[config_object])
    configure_languages(app)
    register_assets(app)
    register_extensions(app)
    register_loginmanager(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app

def configure_languages(app):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(os.path.dirname(__name__))
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = os.path.join(base_dir, "static/translations")
    
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
                    CURRENT_LANGUAGE=session.get('language', request.accept_languages.best_match(app.config['LANGUAGES'].keys())))


def register_assets(app):
    """Register Flask assets."""
    from app.util.assets import bundles
    assets = Environment(app)
    assets.register(bundles)

def register_extensions(app):
    """Register Flask extensions."""
    bootstrap.init_app(app)
    db.init_app(app)
    jsglue.init_app(app)
    babel.init_app(app)
    #celery = create_celery_app(app)
    
def register_loginmanager(app):
    """Register Flask loginmanager."""
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from flask_babel import lazy_gettext as _l
    login_manager.login_message = _l('Please log in to access this page.')
    from app.models.model import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == str(user_id)).first()

def register_blueprints(app):
    """Register Flask blueprints."""
    from app.views.main import main as main_blueprint
    from app.views.auth import auth as auth_blueprint
    from app.views.forms import forms as forms_blueprint
    from app.views.queries import queries as queries_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(forms_blueprint)
    app.register_blueprint(queries_blueprint)
    
def register_errorhandlers(app):
    """Creating and Register Flask error handlers."""
    def page_not_found(e):
          return render_template('error-handling/404.html'), 404

    def internal_error(e):
        return render_template('error-handling/500.html'), 500

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_error)