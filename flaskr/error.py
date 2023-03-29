from flask import jsonify


def bad_request(e):
    # note that we set the 404 status explicitly
    return jsonify({'error': e.description['error']}), 400
