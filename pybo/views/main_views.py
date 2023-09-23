from flask import Blueprint, url_for, jsonify


bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return 'Hello, Pybo!'


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

