import requests
from bs4 import BeautifulSoup
import wikipediaapi
import re

wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (merlin@example.com)', 'en')


def get_info_and_image(page_title, lang='en'):
    """
    Wikipedia 페이지에서 "Place of origin" 정보와 이미지 URL을 가져오는 함수

    Parameters:
        page_title (str): 정보를 가져올 위키백과 페이지의 제목
        lang (str): 위키백과 페이지의 언어 코드 (예: 'en'은 영어)

    Returns:
        tuple: ("Place of origin" 정보, 이미지 URL). 정보를 찾을 수 없으면 해당 부분은 빈 문자열로 반환
    """
    # Wikipedia 페이지의 URL 구성
    url = f"https://{lang}.wikipedia.org/wiki/{page_title}"

    # 페이지 내용을 가져옴
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # "Place of origin" 정보를 포함하는 테이블 행을 찾긔 ㅎㅎ
    place_of_origin = ""
    rows = soup.find_all('tr')
    for row in rows:
        header = row.find('th')
        if header and 'Place of origin' in header.get_text():
            # 정보가 있는 셀을 찾아 텍스트를 저장
            cell = row.find('td')
            if cell:
                place_of_origin = cell.get_text(strip=True)
                break

    # 이미지 URL을 찾긔 ㅎㅎ
    infobox_image_tag = soup.find('td', class_='infobox-image')
    image_url = ""
    if infobox_image_tag:
        img_tag = infobox_image_tag.find('img')
        if img_tag:
            image_url = img_tag['src']
            if not image_url.startswith('http'):  # http 앞에 붙이기
                image_url = "https:" + image_url

    # summary는 api 이용해서 찾긔 ㅎㅎ
    page_py = wiki_wiki.page(page_title)
    summary = page_py.summary[0:]

    # place_origin 특수문자 제거 뿅~!
    place_of_origin = re.sub("[^a-zA-Z, \\\\p{L}]", "", place_of_origin)
    return place_of_origin, image_url, summary
