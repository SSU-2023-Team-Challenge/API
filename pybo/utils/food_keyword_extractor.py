import os
import io
import openai
from google.cloud import vision
import random
import ast
import re

from werkzeug.datastructures import file_storage

random_seed = 42
random.seed(random_seed)


def clean_list(menu_list):
    cleaned_list = []
    for menu in menu_list:
        cleaned = re.sub(r'[^a-zA-Z0-9ㄱ-ㅎㅏ-ㅣ가-힣\s]', '', menu)
        cleaned_list.append(cleaned)

    return cleaned_list


def extract_menu_from_image(img_path):
    # 구글 비젼 키랑 채찍피티 키! 여기있졍
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/kang-youngmin/projects/myproject/pybo/utils/tough-transport-396505-0f2b11b6df13.json'
    openai.api_key = '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'

    # Google Vision - OCR
    client_options = {'api_endpoint': 'eu-vision.googleapis.com'}
    client = vision.ImageAnnotatorClient(client_options=client_options)
    content = img_path.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # 채찍피티 for 음식인식~
    model = "gpt-3.5-turbo"
    query = texts[0].description
    messages = [
        {"role": "system", "content": "You are a food word detector."},
        {"role": "user",
         "content": "나는 너에게 메뉴판 사진에서 인식한 문자열을 입력할거야. 즉 메뉴에 해당하는 음식 문자열이 고정적으로 있고, 음식 설명이 있을 수 도 있고, 없을 수 도 있어. 메뉴에 해당하는 음식들만 딱 리스트로 출력해서 알려줘. 즉 내가 너에게 주는 메뉴 문자열이 입력이고 출력은 여기서 메뉴 음식에 해당하는 문자열만 리스트로 만들어 나에게 보여주는거야. 대답은 하지마. 또한 너의 답변은 파이썬 리스트 형식으로 제공해줘"},
        {"role": "user", "content": query}
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.2
    )

    answer = response['choices'][0]['message']['content']
    menu_list = ast.literal_eval(answer)
    menu_list = clean_list(menu_list)
    return menu_list