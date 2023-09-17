from flask import Blueprint, request, jsonify
from pybo import db
from pybo.models import FoodList, Food, FoodDetail

bp = Blueprint('food', __name__, url_prefix='/food')


@bp.route('/', methods=['GET'], strict_slashes=False)
def get_food_list():
    food_lists = FoodList.query.all()
    return jsonify([fl.name for fl in food_lists])


@bp.route('/getAll', methods=['GET'], strict_slashes=False)
def get_food_and_details():
    foods = Food.query.all()
    food_details = FoodDetail.query.all()

    food_dict = {}
    for food in foods:
        for detail in food_details:
            if food.id == detail.food_id:  # Food와 FoodDetail이 같은 food_id를 가지고 있는 경우
                food_dict[food.name] = {
                    'description': detail.description,
                    'nutrients': detail.nutrients
                }

    return jsonify(food_dict)


@bp.route('/<string:food_name>', methods=['GET'], strict_slashes=False)
def get_food_by_name(food_name):
    food = Food.query.filter_by(name=food_name).first_or_404()
    food_detail = FoodDetail.query.filter_by(food=food).first()

    result = {
        'food_name': food.name,
        'description': food_detail.description,
        'nutrients': food_detail.nutrients
    }

    return jsonify(result)


@bp.route('/<string:list_name>', methods=['GET'])
def get_foods_by_list_name(list_name):
    food_list = FoodList.query.filter_by(name=list_name).first_or_404()
    foods = Food.query.filter_by(food_list=food_list).all()
    return jsonify([food.name for food in foods])


@bp.route('/<string:list_name>/<string:food_name>', methods=['GET'])
def get_food_detail_by_food_name(list_name, food_name):
    food_list = FoodList.query.filter_by(name=list_name).first_or_404()
    food = Food.query.filter_by(name=food_name, food_list=food_list).first_or_404()
    food_detail = FoodDetail.query.filter_by(food=food).first()

    if not food_detail:
        return jsonify({'message': 'Food detail not found'}), 404

    result = {
        'food_name': food.name,
        'description': food_detail.description,
        'nutrients': food_detail.nutrients
    }
    return jsonify(result)


# 새로운 FoodList를 생성하는 함수
@bp.route('/add', methods=['POST'])
def add_food_list():
    data = request.get_json()
    list_name = data.get('list_name')

    if not list_name:
        return jsonify({'message': 'list_name is required'}), 400

    # 이름이 중복되는지 확인
    existing_list = FoodList.query.filter_by(name=list_name).first()
    if existing_list:
        return jsonify({'message': 'List name already exists'}), 400

    new_food_list = FoodList(name=list_name)
    db.session.add(new_food_list)
    db.session.commit()

    return jsonify({'message': 'Successfully added food list'})


@bp.route('/<string:list_name>/add', methods=['POST'])
def add_food(list_name):
    food_list = FoodList.query.filter_by(name=list_name).first_or_404()
    data = request.get_json() # 클라이언트로부터 받은 JSON 데이터를 파이썬 딕셔너리로 변환
    food_name = data.get('food_name')

    # error 처리 None 이거나 빈 문자열 ("") 등 "falsy"한 값인 경우
    if not food_name:
        return jsonify({'message': 'food_name is required'}), 400

    new_food = Food(name=food_name, food_list=food_list)
    db.session.add(new_food)
    db.session.commit()

    return jsonify({'message': 'Successfully added food'})


@bp.route('/<string:list_name>/<string:food_name>/add_detail', methods=['POST'])
def add_food_detail(list_name, food_name):
    food_list = FoodList.query.filter_by(name=list_name).first_or_404()
    food = Food.query.filter_by(name=food_name, food_list=food_list).first_or_404()
    data = request.get_json()
    description = data.get('description')
    nutrients = data.get('nutrients')

    # 여기에 유효성 검사를 추가할 수 있습니다.
    if not description or not nutrients:
        return jsonify({'message': 'description and nutrients are required'}), 400

    food_detail = FoodDetail(food=food, description=description, nutrients=nutrients)
    db.session.add(food_detail)
    db.session.commit()

    return jsonify({'message': 'Successfully added food detail'})


# FoodList 이름을 수정하는 함수
@bp.route('/<string:list_name>/update', methods=['PUT'])
def update_food_list_name(list_name):
    food_list = FoodList.query.filter_by(name=list_name).first_or_404()
    data = request.get_json()
    new_name = data.get('new_name')

    if not new_name:
        return jsonify({'message': 'new_name is required'}), 400

    food_list.name = new_name
    db.session.commit()

    return jsonify({'message': 'Successfully updated food list name'})


# Food 이름을 수정하는 함수
@bp.route('/<string:list_name>/<string:food_name>/update', methods=['PUT'])
def update_food_name(list_name, food_name):
    food = Food.query.join(FoodList).filter(
        FoodList.name == list_name,
        Food.name == food_name
    ).first_or_404()

    data = request.get_json()
    new_name = data.get('new_name')

    if not new_name:
        return jsonify({'message': 'new_name is required'}), 400

    food.name = new_name
    db.session.commit()

    return jsonify({'message': 'Successfully updated food name'})


# FoodDetail을 수정하는 함수
@bp.route('/<string:list_name>/<string:food_name>/update_detail', methods=['PUT'])
def update_food_detail(list_name, food_name):
    food = Food.query.join(FoodList).filter(
        FoodList.name == list_name,
        Food.name == food_name
    ).first_or_404()

    food_detail = FoodDetail.query.filter_by(food=food).first_or_404()

    data = request.get_json()
    description = data.get('description')
    nutrients = data.get('nutrients')

    if description:
        food_detail.description = description
    if nutrients:
        food_detail.nutrients = nutrients

    db.session.commit()

    return jsonify({'message': 'Successfully updated food detail'})


# FoodList를 삭제하는 함수
@bp.route('/<string:list_name>/delete', methods=['DELETE'])
def delete_food_list(list_name):
    food_list = FoodList.query.filter_by(name=list_name).first_or_404()

    # FoodList에 속한 모든 Food와 FoodDetail을 먼저 삭제
    foods = Food.query.filter_by(food_list=food_list).all()
    for food in foods:
        food_detail = FoodDetail.query.filter_by(food=food).first()
        if food_detail:
            db.session.delete(food_detail)
        db.session.delete(food)

    db.session.delete(food_list)  # 마지막으로 FoodList 삭제
    db.session.commit()

    return jsonify({'message': 'Successfully deleted food list and all its contents'})


# Food를 삭제하는 함수
@bp.route('/<string:list_name>/<string:food_name>/delete', methods=['DELETE'])
def delete_food(list_name, food_name):
    food_list = FoodList.query.filter_by(name=list_name).first_or_404()
    food = Food.query.filter_by(name=food_name, food_list=food_list).first_or_404()

    # 해당 음식에 연결된 FoodDetail 객체가 있는지 확인
    food_detail = FoodDetail.query.filter_by(food=food).first()
    if food_detail:
        db.session.delete(food_detail)  # 있으면 FoodDetail 먼저 삭제

    db.session.delete(food)  # 이후 Food 삭제
    db.session.commit()

    return jsonify({'message': 'Successfully deleted food and its details'})


# FoodDetail을 삭제하는 함수
@bp.route('/<string:list_name>/<string:food_name>/delete_detail', methods=['DELETE'])
def delete_food_detail(list_name, food_name):
    food = Food.query.join(FoodList).filter(
        FoodList.name == list_name,
        Food.name == food_name
    ).first_or_404()

    food_detail = FoodDetail.query.filter_by(food=food).first_or_404()

    db.session.delete(food_detail)
    db.session.commit()

    return jsonify({'message': 'Successfully deleted food detail'})
