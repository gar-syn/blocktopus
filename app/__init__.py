from flask import Flask, render_template
from flask_assets import Environment
from flask_sqlalchemy import SQLAlchemy
from whitenoise import WhiteNoise
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from .util import config

db = SQLAlchemy()

def page_not_found(e):
      return render_template('404.html'), 404

def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    
    from .util.assets import bundles
    assets = Environment(app)
    assets.register(bundles)

    app.register_error_handler(404, page_not_found)

    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # blueprint for main routes
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for auth routes 
    from .routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    # blueprint for forms routes
    from .routes.forms import forms as forms_blueprint
    app.register_blueprint(forms_blueprint)
    
    return app

db.create_all(app=create_app())