from flask import Blueprint, url_for, jsonify


bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    return '메뉴판 인식을 통한 음식 API'
