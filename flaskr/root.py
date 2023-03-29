from flask import Blueprint, jsonify, request, abort, current_app
from flaskr.__init__ import TRANSCRIBER

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

    TRANSCRIBER.get_and_store_transcript(video_id)

    return jsonify()
