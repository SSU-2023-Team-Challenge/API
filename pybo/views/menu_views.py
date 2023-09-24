from flask import Blueprint, request, jsonify
from pybo import db
from pybo.models import MenuName, MenuDescription, MenuImage

bp = Blueprint('menu', __name__, url_prefix='/menu')


@bp.route('/getAll', methods=['GET'], strict_slashes=False)
def get_all_menus():
    menus = MenuName.query.all()
    menu_dict = {}
    for menu in menus:
        description = menu.description
        if description:
            menu_dict[menu.name] = {
                'description': description.description,
                'nutrients': description.nutrients
            }

    return jsonify(menu_dict)


@bp.route('/<string:menu_name>', methods=['GET'], strict_slashes=False)
def get_menu_by_name(menu_name):
    menu = MenuName.query.filter_by(name=menu_name).first_or_404()
    description = menu.description
    if not description:
        return jsonify({'message': 'Menu description not found'}), 404

    result = {
        'menu_name': menu.name,
        'description': description.description,
        'nutrients': description.nutrients
    }

    return jsonify(result)


@bp.route('/add', methods=['POST'])
def add_menu():
    data = request.get_json()
    menu_name = data.get('menu_name')

    if not menu_name:
        return jsonify({'message': 'menu_name is required'}), 400

    existing_menu = MenuName.query.filter_by(name=menu_name).first()
    if existing_menu:
        return jsonify({'message': 'Menu name already exists'}), 400

    new_menu = MenuName(name=menu_name)
    db.session.add(new_menu)
    db.session.commit()

    return jsonify({'message': 'Successfully added menu'})


@bp.route('/<string:menu_name>/add_description', methods=['POST'])
def add_menu_description(menu_name):
    menu = MenuName.query.filter_by(name=menu_name).first_or_404()
    data = request.get_json()
    description_text = data.get('description')
    nutrients = data.get('nutrients')

    if not description_text or not nutrients:
        return jsonify({'message': 'description and nutrients are required'}), 400

    description = MenuDescription(menu_name_id=menu.id, description=description_text, nutrients=nutrients)
    db.session.add(description)
    db.session.commit()

    return jsonify({'message': 'Successfully added menu description'})


@bp.route('/<string:menu_name>/update', methods=['PUT'])
def update_menu_name(menu_name):
    menu = MenuName.query.filter_by(name=menu_name).first_or_404()
    data = request.get_json()
    new_name = data.get('new_name')

    if not new_name:
        return jsonify({'message': 'new_name is required'}), 400

    menu.name = new_name
    db.session.commit()

    return jsonify({'message': 'Successfully updated menu name'})


@bp.route('/<string:menu_name>/update_description', methods=['PUT'])
def update_menu_description(menu_name):
    menu = MenuName.query.filter_by(name=menu_name).first_or_404()
    description = menu.description

    data = request.get_json()
    description_text = data.get('description')
    nutrients = data.get('nutrients')

    if description_text:
        description.description = description_text
    if nutrients:
        description.nutrients = nutrients

    db.session.commit()

    return jsonify({'message': 'Successfully updated menu description'})


@bp.route('/<string:menu_name>/delete', methods=['DELETE'])
def delete_menu(menu_name):
    menu = MenuName.query.filter_by(name=menu_name).first_or_404()
    description = menu.description
    if description:
        db.session.delete(description)
    db.session.delete(menu)
    db.session.commit()

    return jsonify({'message': 'Successfully deleted menu and its description'})


@bp.route('/<string:menu_name>/delete_description', methods=['DELETE'])
def delete_menu_description(menu_name):
    menu = MenuName.query.filter_by(name=menu_name).first_or_404()
    description = menu.description

    if not description:
        return jsonify({'message': 'Description not found'}), 404

    db.session.delete(description)
    db.session.commit()

    return jsonify({'message': 'Successfully deleted menu description'})


from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# 파일 확장자 확인
def allowed_file(filename):
    """허용된 파일 확장자인지 확인합니다."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/<string:menu_name>/add_image', methods=['POST'])
def add_menu_image(menu_name):
    """특정 메뉴에 이미지를 추가합니다."""
    menu = MenuName.query.filter_by(name=menu_name).first_or_404()
    file = request.files.get('image')

    if 'image' not in request.files:
        return jsonify({'message': '이미지 파일이 필요합니다'}), 400

    if file.filename == '':
        return jsonify({'message': '선택된 이미지 파일이 없습니다'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        image = MenuImage(filename=filename, menu_name=menu)
        db.session.add(image)
        db.session.commit()
        return jsonify({'message': '메뉴 이미지가 성공적으로 추가되었습니다'})
    else:
        return jsonify({'message': '허용되지 않은 파일 형식입니다'}), 400
