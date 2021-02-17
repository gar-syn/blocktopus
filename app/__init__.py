import os
from flask import Flask, render_template
from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
from whitenoise import WhiteNoise
from . import config
from flask_login import LoginManager

db = SQLAlchemy()

def page_not_found(e):
      return render_template('404.html'), 404

def create_app():
    app = Flask(__name__)
    
    #Flask Assets Bundle
    from .util.assets import bundles
    assets = Environment(app)
    assets.register(bundles)

    app.register_error_handler(404, page_not_found)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

db.create_all(app=create_app())