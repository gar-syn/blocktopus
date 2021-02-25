import os
from flask import Flask, render_template
from flask_assets import Environment
from flask_sqlalchemy import SQLAlchemy
from whitenoise import WhiteNoise
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_jsglue import JSGlue

from .util.config import DevConfig

db = SQLAlchemy()

def page_not_found(e):
      return render_template('error-handling/404.html'), 404

def internal_error(e):
      return render_template('error-handling/500.html'), 500

def create_app(config_object=DevConfig):
    app = Flask(__name__)
    
    from .util.assets import bundles
    assets = Environment(app)
    assets.register(bundles)
    
    app.config.from_object(config_object)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_error)
    
    #Serving static files with WhiteNoise
    WHITENOISE_MAX_AGE = 31536000 if not app.config["DEBUG"] else 0
    app.wsgi_app = WhiteNoise(
        app.wsgi_app,
        root=os.path.join(os.path.dirname(__file__), "static"),
        prefix="static/",
        max_age=WHITENOISE_MAX_AGE,
    )    
    static_folders = (
        os.path.join(os.path.dirname(__file__), "static/gen/css"),
        os.path.join(os.path.dirname(__file__), "static/gen/js"),
        os.path.join(os.path.dirname(__file__), "static/fonts/")
        )
    for static in static_folders:
        app.wsgi_app.add_files(static)
    
    Bootstrap(app)
    jsglue = JSGlue(app)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    # blueprint for routes
    from .main import main as main_blueprint
    from .views.auth import auth as auth_blueprint
    from .views.forms import forms as forms_blueprint
    from .views.queries import queries as queries_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(forms_blueprint)
    app.register_blueprint(queries_blueprint)
    
    return app

db.create_all(app=create_app())