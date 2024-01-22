# Third-party Imports
from flask import Flask

# Local Imports
from re_search.params import PARAMS

class DefaultConfig:
    UPLOAD_FOLDER = PARAMS['UPLOAD_FOLDER']


def create_app(config=None): 
    app = Flask(__name__)
    config = DefaultConfig if not config else config
    app.config.from_object(config)

    from .routes.main import main
    app.register_blueprint(main, url_prefix='/')
    
    return app