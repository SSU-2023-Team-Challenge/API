# add_menu_data.py

from pybo import db, create_app  # 'your_flask_app'는 애플리케이션의 모듈 이름으로 교체해주세요.
from pybo.models import MenuName, MenuDescription  # 'models'는 해당 모델들이 정의된 모듈의 이름입니다.
from datetime import datetime


def add_data_to_db():
    current_time = datetime.now()  # 현재 날짜 및 시간을 가져옵니다.

    # 카이막 데이터
    kaymak = MenuName(name="하와이안 피자", create_date=current_time)
    kaymak_description = MenuDescription(
        description="파인애플 토핑이 특징인 피자. 일명 파인애플 피자다.",
        nutrients="파인애플, 햄, 치즈, 토마토 소스",
        create_date = current_time
    )
    kaymak.description = kaymak_description
    db.session.add(kaymak)

    # 하와이안 피자 데이터
    hawaiian_pizza = MenuName(name="하와이안 피자", create_date=current_time)
    hawaiian_pizza_description = MenuDescription(
        description="파인애플 토핑이 특징인 피자. 일명 파인애플 피자다.",
        nutrients="파인애플, 햄, 치즈, 토마토 소스",
        create_date=current_time
    )
    hawaiian_pizza.description = hawaiian_pizza_description
    db.session.add(hawaiian_pizza)

    db.session.commit()
    print("데이터 추가 완료!")


if __name__ == "__main__":
    app = create_app()
    app.config.from_object('config.development')
    with app.app_context():  # 앱 컨텍스트 내에서 DB 작업 수행
        add_data_to_db()
