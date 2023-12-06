# Third-party Imports
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager

# Local Imports
from re_search.params import PARAMS

# db = SQLAlchemy()
# bcrypt = Bcrypt()
# signup_token = PARAMS['TOKEN']

class DefaultConfig:
    pass
    # SECRET_KEY = PARAMS['SECRET_KEY']
    # SQLALCHEMY_DATABASE_URI = PARAMS['DB_URI']


def create_app(config=None): 
    app = Flask(__name__)
    config = DefaultConfig if not config else config
    app.config.from_object(config)
    # db.init_app(app)
    # bcrypt.init_app(app)

    from .routes.main import main
    from .routes.auth import auth
    from .routes.errors import errors

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(errors, url_prefix='/')
    
    # with app.app_context():
    #     db.create_all()

    # login_manager = LoginManager()
    # login_manager.login_view = 'routes/auth.login'
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(int(id))
    
    return app