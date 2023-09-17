from pybo import db
from datetime import datetime


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)


class MenuImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    upload_date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    # 이 부분에 추출된 키워드를 저장할 필드를 추가할 수도 있습니다.


#각 Food 객체는 .detail을 통해 FoodDetail 정보를 얻을 수 있고, FoodList 객체는 .foods를 통해 속해 있는 Food 객체들을 얻을 수 있음.
class FoodList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    # 역참조 설정: 하나의 FoodList에는 여러 개의 Food가 있을 수 있음
    foods = db.relationship('Food', backref='food_list', lazy=True)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    food_list_id = db.Column(db.Integer, db.ForeignKey('food_list.id'), nullable=False)

    # 역참조 설정: 하나의 Food에는 하나의 FoodDetail만 있을 수 있음
    detail = db.relationship('FoodDetail', backref='food', lazy=True, uselist=False)


class FoodDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text(), nullable=True)
    nutrients = db.Column(db.Text(), nullable=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)

