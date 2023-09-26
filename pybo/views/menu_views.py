from flask import Blueprint, request, jsonify
from pybo import db
from pybo.models import Menu, MenuDescription, MenuImage

bp = Blueprint('menu', __name__, url_prefix='/menu')


@bp.route('/getAll', methods=['GET'], strict_slashes=False)
def get_all_menus():
    menus = Menu.query.all()

    if not menus:  # 메뉴가 전혀 없는 경우
        return jsonify({
            'message': 'No menus found.'
        }), 404

    menu_dict = {}
    for menu in menus:
        menu_name = menu.name

        if menu.description:
            description = menu.description
        else:
            description = 'Menu description not found'

        if menu.image_url and menu.image_url.strip():
            image_url = menu.image_url
        else:
            image_url = 'Image URL not found'

        menu_dict[menu_name] = {
            'description': description,
            'image_url': image_url
        }

    return jsonify(menu_dict)


@bp.route('/<string:menu_name>', methods=['GET'], strict_slashes=False)
def get_menu_by_name(menu_name):
    from datetime import datetime

    menu = Menu.query.filter_by(name=menu_name).first_or_404()
    menu.create_date = datetime.now()
    # 초기 메시지 설정
    messages = []
    # 오류 메세지 반환
    # 없을 경우
    if menu.description is None:
        messages.append('Menu description not found')

    if menu.image_url is None or menu.image_url.strip() == "":
        messages.append('Image URL not found')

    if messages:
        return jsonify({'message': ', '.join(messages)}), 404

    result = {
        'description': menu.description,
        'image_url': menu.image_url
    }

    return jsonify(result)


@bp.route('/add', methods=['POST'])
def add_menu():
    data = request.get_json()
    menu = data.get('menu')

    if not menu:
        return jsonify({'message': 'menu is required'}), 400

    existing_menu = Menu.query.filter_by(name=menu).first()
    if existing_menu:
        return jsonify({'message': 'Menu name already exists'}), 400

    new_menu = Menu(name=menu)
    db.session.add(new_menu)
    db.session.commit()

    return jsonify({'message': 'Successfully added menu'})


@bp.route('/<string:menu_name>/add_description_or_imageURL', methods=['POST'])
def add_menu_description_or_imageURL(menu_name):
    menu = Menu.query.filter_by(name=menu_name).first_or_404()
    data = request.get_json()
    description_text = data.get('description')
    image_url = data.get('image_url')  # 이미지 URL 받기

    if not description_text and not image_url:  # 설명과 이미지 URL 모두 없는 경우만 에러 반환
        return jsonify({'message': 'Either description or image_url is required'}), 400

    # 이미 설명이나 이미지 URL이 있는 경우 에러 반환 -> PUT으로 처리해야함.
    if menu.description and menu.image_url: # 설명과 이미지 URL 둘 다 존재
        return jsonify({'message': 'Description and Image URL already exists'}), 400
    elif description_text and menu.description: # 설명만 존재
        return jsonify({'message': 'Description already exists but no Image URL'}), 400
    elif image_url and menu.image_url: # 이미지 URL만 존재
        return jsonify({'message': 'Image URL already exists but no Description'}), 400

    # description_text 또는 image_url이 제공되었는지 확인하고 제공된 경우에만 해당 필드를 업데이트
    if description_text:
        menu.description = description_text
    if image_url:
        menu.image_url = image_url

    db.session.commit()

    return jsonify({'message': 'Successfully added menu information'})


@bp.route('/<string:menu_name>/update', methods=['PUT'])
def update_menu(menu_name):
    menu = Menu.query.filter_by(name=menu_name).first_or_404() # 기존 메뉴 이름이 없는 경우 처리

    data = request.get_json()
    new_name = data.get('new_name')
    # 공백이나 새로운 이름을 입력하지 않은 경우
    if not new_name or new_name.strip() == "":
        return jsonify({'message': "'new_name' is required and cannot be empty"}), 400

    # 새 이름이 이미 있는 메뉴의 이름과 충돌하는지 확인
    existing_menu = Menu.query.filter_by(name=new_name).first()
    if existing_menu:
        return jsonify({'message': 'The new_name already exists for another menu'}), 400

    menu.name = new_name
    db.session.commit()

    return jsonify({'message': 'Successfully updated menu name'})


@bp.route('/<string:menu_name>/update_description', methods=['PUT'])
def update_menu_description_or_imageURL(menu_name):
    menu = Menu.query.filter_by(name=menu_name).first_or_404()

    data = request.get_json()
    description_text = data.get('new_description')
    image_url = data.get('new_image_url')

    # new_description 또는 new_image_url 중 하나라도 입력되지 않았다면 오류 반환
    if not description_text and not image_url:
        return jsonify({'message': "Either 'new_description' or 'new_image_url' is required"}), 400
    # 입력되지 않았거나 공백인 경우 체크
    elif not description_text or description_text.strip() == "":
        return jsonify({'message': 'Description is required and cannot be empty or just whitespace'}), 400
    elif not image_url or image_url.strip() == "":
        return jsonify({'message': 'Image URL is required and cannot be empty or just whitespace'}), 400

    # 원래 설명이나 이미지 URL이 없는 경우의 처리
    if not menu.description and description_text:
        return jsonify({'message': 'Description not found, but a new one is provided'}), 400
    if not menu.image_url and image_url:
        return jsonify({'message': 'Image URL not found, but a new one is provided'}), 400

    # description_text 또는 image_url이 제공되었는지 확인하고 제공된 경우에만 해당 필드를 업데이트
    if description_text:
        menu.description = description_text
    if image_url:
        menu.image_url = image_url

    db.session.commit()

    return jsonify({'message': 'Successfully updated menu information'})


@bp.route('/<string:menu_name>/delete', methods=['DELETE'])
def delete_menu(menu_name):
    menu = Menu.query.filter_by(name=menu_name).first_or_404()

    db.session.delete(menu)
    db.session.commit()

    return jsonify({'message': 'Successfully deleted menu'})


@bp.route('/<string:menu_name>/delete_description_and_imageURL', methods=['DELETE'])
def delete_menu_description_and_imageURL(menu_name):
    menu = Menu.query.filter_by(name=menu_name).first_or_404()

    # 원래 설명이나 이미지 URL이 없는 경우의 처리
    if not menu.description and not menu.image_url:
        return jsonify({'message': 'Description and Image URL not found'}), 400
    elif not menu.description :
        return jsonify({'message': 'Description not found'}), 400
    elif not menu.image_url :
        return jsonify({'message': 'Image URL not found'}), 400

    if menu.description:
        menu.description = None
    if menu.image_url:
        menu.image_url = None

    db.session.commit()

    return jsonify({'message': 'Successfully deleted menu description and image URL'})


@bp.route('/<string:menu_name>/delete_description', methods=['DELETE'])
def delete_menu_description(menu_name):
    menu = Menu.query.filter_by(name=menu_name).first_or_404()

    # 원래 설명이나 이미지 URL이 없는 경우의 처리
    if not menu.description :
        return jsonify({'message': 'Description not found'}), 400

    if menu.description:
        menu.description = None

    db.session.commit()

    return jsonify({'message': 'Successfully deleted menu description'})


@bp.route('/<string:menu_name>/delete_imageURL', methods=['DELETE'])
def delete_menu_imageURL(menu_name):
    menu = Menu.query.filter_by(name=menu_name).first_or_404()

    # 원래 설명이나 이미지 URL이 없는 경우의 처리
    if not menu.image_url :
        return jsonify({'message': 'Image URL not found'}), 400

    if menu.image_url:
        menu.image_url = None

    db.session.commit()

    return jsonify({'message': 'Successfully deleted menu image URL'})


from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


# 파일 확장자 확인
def allowed_file(filename):
    """허용된 파일 확장자인지 확인합니다."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/<string:menu>/add_image', methods=['POST'])
def add_menu_image(menu):
    menu = Menu.query.filter_by(name=menu).first_or_404()
    file = request.files.get('image')

    if 'image' not in request.files:
        return jsonify({'message': '이미지 파일이 필요합니다'}), 400

    if file.filename == '':
        return jsonify({'message': '선택된 이미지 파일이 없습니다'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        image = MenuImage(filename=filename, menu_id=menu.id)  # menu_id로 변경
        db.session.add(image)
        db.session.commit()
        return jsonify({'message': '메뉴 이미지가 성공적으로 추가되었습니다'})
    else:
        return jsonify({'message': '허용되지 않은 파일 형식입니다'}), 400
