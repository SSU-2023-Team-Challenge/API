from pybo import db
from datetime import datetime


class MenuBoardImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    upload_date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)


class MenuName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)

    # 역참조 설정을 보다 직관적으로 변경
    descriptions = db.relationship('MenuDescription', backref='menu', lazy=True)
    images = db.relationship('MenuImage', backref='menu', lazy=True)


class MenuDescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text(), nullable=True)
    nutrients = db.Column(db.Text(), nullable=True)
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)

    # ForeignKey 설정
    menu_name_id = db.Column(db.Integer, db.ForeignKey('menu_name.id'), nullable=False)


class MenuImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    created_date = db.Column(db.DateTime(), default=datetime.utcnow)

    # ForeignKey 설정
    menu_name_id = db.Column(db.Integer, db.ForeignKey('menu_name.id'), nullable=False)
