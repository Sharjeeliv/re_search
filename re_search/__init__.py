# Third-party Imports
from flask import Flask
from celery import Celery

# Local Imports
from re_search.params import PARAMS


class DefaultConfig:
    UPLOAD_FOLDER = PARAMS['UPLOAD_FOLDER']
    SECRET_KEY = PARAMS['SECRET_KEY']

def create_app(config=None): 
    app = Flask(__name__)
    config = DefaultConfig if not config else config
    app.config.from_object(config)

    from .routes.main import main
    app.register_blueprint(main, url_prefix='/')
    
    return app