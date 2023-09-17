from flask import Blueprint, url_for, jsonify
from werkzeug.utils import redirect
from google.cloud import firestore

import pyrebase

bp = Blueprint('main', __name__, url_prefix='/')

## firebasecode -------------------------
# config = {
#     "apiKey": "AIzaSyCcopjipq8SnnMeuJ8Ldshqn8rIFg8YnmI",
#     "authDomain": "test-2cb4d.firebaseapp.com",
#     "databaseURL": "https://test-2cb4d-default-rtdb.firebaseio.com",
#     "projectId": "test-2cb4d",
#     "storageBucket": "test-2cb4d.appspot.com",
#     "messagingSenderId": "403442603631",
#     "appId": "1:403442603631:web:b6b12a6e6b99cc14189f9a",
#     "measurementId": "G-F2JR2Y883C"
# }
# firebase = pyrebase.initialize_app(config)
# db = firestore.Client.from_service_account_json("/Users/kang-youngmin/Downloads/test-2cb4d-firebase-adminsdk-sqi07-db3881ff09.json")  # 여기에 서비스 계정 키의 경로를 입력하세요.
## firebasecode -------------------------
# @bp.route('/get_products', methods=['GET'])
# def get_products():
#     products_ref = db.collection('product')
#     products = {}
#     for product_doc in products_ref.str
#     eam():
#         product_id = product_doc.id
#         product_data = product_doc.to_dict()
#         products[product_id] = product_data
#
#     return jsonify(products)


@bp.route('/')
def index():
    #return redirect(url_for('question._list'))
    return 'Hello, Pybo!'


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'


# @bp.route('/test', methods=['GET'])
# def index():
#     return 'Hello, Pybo!'

