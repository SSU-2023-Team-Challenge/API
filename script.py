from pybo import db
from pybo.models import FoodList, Food, FoodDetail
from datetime import datetime

# FoodList를 생성합니다.
food_list = FoodList(name="My Food List", create_date=datetime.now())

# Food와 FoodDetail을 생성하고 연결합니다.
foods_data = [
    {"name": "고구마 맛탕", "description": "맛탕은 한입크기로 썰어 튀긴 고구마, 당근, 감자, 옥수수 등에 설탕과 물엿을 졸여 만든 시럽을 입힌 음식이다. 고구마 맛탕은 고구마로 만든 맛탕이다."},
    {"name": "카이막", "description": "카이막(Kaymak)은 튀르키예의 음식으로 우유의 지방을 모아 굳혀 크림처럼 만든 유제품이다. 주로 꿀을 곁들여 빵과 함께 먹는다."},
    {"name": "아이바르", "description": "아이바르는 주로 붉은 피망으로 만든 후추 기반 조미료이다. 그것은 또한 마늘, 가지 및 고추를 포함할지도 모른다."},
    {"name": "파니르", "description": "물소젖으로 만든 남아시아의 전통 치즈이자 산으로 응고한 치즈 중 하나이며, 인도, 네팔, 방글라데시, 파키스탄, 아프가니스탄, 스리랑카에서 먹는다."},
]

# Food와 FoodDetail 객체를 생성하고 FoodList에 연결합니다.
for food_data in foods_data:
    food = Food(name=food_data["name"])
    food_detail = FoodDetail(description=food_data["description"])

    food.detail = food_detail  # Food와 FoodDetail을 연결합니다.
    food_list.foods.append(food)  # FoodList와 Food을 연결합니다.

# 데이터베이스에 추가합니다.
db.session.add(food_list)
db.session.commit()

