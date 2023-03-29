from flask import Flask
from flask_cors import CORS
from flaskr.error import bad_request
from flaskr import root
from pathlib import Path
from flaskr import transcriber
from flaskr import llm_store

TRANSCRIBER = transcriber.Transcriber()
LLM_STORE = llm_store.LLMStore()


def create_app():
    """
    Creates an app instance. We assume an "instance" folder already exists.
    """

    # Create and config the app.
    app = Flask(__name__, instance_relative_config=True)

    # We always require a config file to run.
    if not app.config.from_pyfile('config.py'):
        raise FileNotFoundError()

    if 'DATA_DIRECTORY_PATH' not in app.config:
        raise ValueError('Data directory path missing from the config')

    # Creates the directory that will house the transcripts and LLM indices for each transcript.
    data_dir = Path(app.config['DATA_DIRECTORY_PATH'])
    data_dir.mkdir(parents=True, exist_ok=True)
    TRANSCRIBER.set_data_path(data_dir)
    LLM_STORE.set_data_path(data_dir)

    # To support cross-origin requests. This will handle the headers required.
    CORS(app)
    # Register error handlers across blueprints.
    app.register_error_handler(400, bad_request)

    # Register info related routes.
    app.register_blueprint(root.bp)

    return app
