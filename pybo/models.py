from pybo import db
from datetime import datetime


class MenuBoardImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    upload_date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)


class MenuName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    # 역참조 설정
    description = db.relationship('MenuDescription', backref='menu_name', lazy=True, uselist=False)
    image = db.relationship('MenuImage', backref='menu_name', lazy=True, uselist=False)


class MenuDescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text(), nullable=True)
    nutrients = db.Column(db.Text(), nullable=True)

    # ForeignKey 설정
    menu_name_id = db.Column(db.Integer, db.ForeignKey('menu_name.name'), nullable=False)


class MenuImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)  # 이미지 파일 이름 필드를 추가했습니다.

    # ForeignKey 설정
    menu_name_id = db.Column(db.Integer, db.ForeignKey('menu_name.name'), nullable=False)
