from pybo import db
from datetime import datetime
from sqlalchemy import Text


class MenuBoardImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=True)  # 요약 설명으로 사용
    place_of_origin = db.Column(Text, nullable=True)  # 원산지
    image_url = db.Column(db.String(3000))
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)

    descriptions = db.relationship('MenuDescription', backref='menu', lazy=True)
    images = db.relationship('MenuImage', backref='menu', lazy=True)


class MenuDescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text(), nullable=True)
    nutrients = db.Column(db.Text(), nullable=True)
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)

    # ForeignKey 설정
    menu_name_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)


class MenuImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    created_date = db.Column(db.DateTime(), default=datetime.utcnow)

    # ForeignKey 설정
    menu_name_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
