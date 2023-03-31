from flask import Blueprint, jsonify, request, abort, current_app
from flaskr import app_constants

bp = Blueprint('root', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def root():
    """Returns a sanity check about the server running."""
    return jsonify({'output': 'Welcome to YT transcript bot server'})


@bp.route('/create-bot', methods=['POST'])
def create_bot():
    """Creates a bot for a video."""
    request_json = request.get_json()
    if not request_json:
        abort(400, {'error': 'no JSON data in the request'})

    video_id = request_json.get('video_id')
    if not video_id:
        abort(400, {'error': 'video id not provided'})

    llm_store = current_app.config[app_constants.LLM_STORE_KEY]
    try:
        llm_store.get_model(video_id)
    except FileNotFoundError as _:
        print(f'Creating new model for {video_id}')
        # First transcribe the video and then create the model.
        transcriber = current_app.config[app_constants.TRANSCRIBER_KEY]
        transcriber.get_and_store_transcript(video_id)
        llm_store.create_model(video_id)
    return jsonify()


@bp.route('/ask-bot', methods=['POST'])
def ask_bot():
    """Asks a query for a bot created from a video."""
    request_json = request.get_json()
    if not request_json:
        abort(400, {'error': 'no JSON data in the request'})

    video_id = request_json.get('video_id')
    if not video_id:
        abort(400, {'error': 'video id not provided'})

    query = request_json.get('query')
    if not query:
        abort(400, {'error': 'query is not provided'})

    llm_store = current_app.config[app_constants.LLM_STORE_KEY]
    try:
        llm_index = llm_store.get_model(video_id)
    except FileNotFoundError as exception:
        abort(400, {'error': f'{exception}'})

    response = llm_index.query(query)
    print(f'{video_id} Query: {query} Response: {response}')
    return jsonify({'response': str(response)})
