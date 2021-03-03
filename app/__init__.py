import os
from flask import Flask, render_template
from flask_assets import Environment
from flask_login import LoginManager

from .util.config import DevConfig
from .util.extensions import db, jsglue, bootstrap, create_celery_app

def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    register_assets(app)
    register_extensions(app)
    register_loginmanager(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app

def register_assets(app):
    """Register Flask assets."""
    from .util.assets import bundles
    assets = Environment(app)
    assets.register(bundles)

def register_extensions(app):
    """Register Flask extensions."""
    bootstrap.init_app(app)
    db.init_app(app)
    jsglue.init_app(app)
    #celery = create_celery_app(app)
    
def register_loginmanager(app):
    """Register Flask loginmanager."""
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from .models.model import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

def register_blueprints(app):
    """Register Flask blueprints."""
    from .views.main import main as main_blueprint
    from .views.auth import auth as auth_blueprint
    from .views.forms import forms as forms_blueprint
    from .views.queries import queries as queries_blueprint
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

db.create_all(app=create_app())