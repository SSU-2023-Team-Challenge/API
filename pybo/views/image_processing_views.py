from flask import request, redirect, url_for, render_template, Blueprint
from werkzeug.utils import secure_filename
from pybo import db
from pybo.models import MenuImage
import os

bp = Blueprint('image', __name__, url_prefix='/image')

UPLOAD_FOLDER = 'static/uploads'


@bp.route('/')
def upload_form():
    return render_template('image/image_test.html')


@bp.route('/upload', methods=['POST'])
def upload_file():
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            # 파일을 업로드할 경로 설정
            filepath = os.path.join(bp.config['UPLOAD_FOLDER'], secure_filename(photo.filename))
            photo.save(filepath)

            # 데이터베이스에 파일 정보 저장
            new_image = MenuImage(filename=secure_filename(photo.filename))
            db.session.add(new_image)
            db.session.commit()

            return '사진이 업로드되었습니다.'

# @bp.route('/', methods=['POST'])
# def upload_file():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file:
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(UPLOAD_FOLDER, filename))
#
#             new_image = MenuImage(filename=filename)
#             db.session.add(new_image)
#             db.session.commit()
#
#             # 사진 키워드 관련 코드 호출.
#
#             return redirect(url_for('uploaded_file', filename=filename))
