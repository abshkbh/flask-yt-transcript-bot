from flask import Blueprint, jsonify

bp = Blueprint('root', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def root():
    """Returns a sanity check about the server running."""
    return jsonify({'output': 'Welcome to YT transcript bot server'})
