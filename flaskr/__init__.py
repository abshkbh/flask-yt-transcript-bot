from flask import Flask
from flask_cors import CORS
from flaskr.error import bad_request
from flaskr import root


def create_app():
    """
    Creates an app instance. We assume an "instance" folder already exists.
    """

    # Create and config the app.
    app = Flask(__name__, instance_relative_config=True)

    # We always require a config file to run.
    if not app.config.from_pyfile('config.py'):
        raise FileNotFoundError()

    # To support cross-origin requests. This will handle the headers required.
    CORS(app)
    # Register error handlers across blueprints.
    app.register_error_handler(400, bad_request)

    # Register info related routes.
    app.register_blueprint(root.bp)

    return app
