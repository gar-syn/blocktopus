from flask import Flask, render_template
from flask_assets import Environment
from flask_sqlalchemy import SQLAlchemy
from whitenoise import WhiteNoise
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from .util.config import DevConfig

db = SQLAlchemy()

def page_not_found(e):
      return render_template('error-handling/404.html'), 404

def internal_error(e):
      return render_template('error-handling/500.html'), 500

def create_app(config_object=DevConfig):
    app = Flask(__name__)
    Bootstrap(app)
    
    from .util.assets import bundles
    assets = Environment(app)
    assets.register(bundles)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_error)

    app.config.from_object(config_object)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    # blueprint for main routes
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for auth routes 
    from .views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    # blueprint for forms routes
    from .views.forms import forms as forms_blueprint
    app.register_blueprint(forms_blueprint)
    
    # blueprint for queries routes
    from .views.queries import queries as queries_blueprint
    app.register_blueprint(queries_blueprint)
    
    return app

db.create_all(app=create_app())