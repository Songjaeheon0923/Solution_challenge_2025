import os
import requests
from dotenv import load_dotenv
from google.generativeai import configure, GenerativeModel

# ✅ .env에서 환경변수 로드
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

if not GEMINI_API_KEY or not PEXELS_API_KEY:
    raise ValueError("API 키가 .env에 설정되어 있지 않습니다.")

# ✅ Gemini API 설정
configure(api_key=GEMINI_API_KEY)
gemini = GenerativeModel("models/gemini-1.5-flash")

# 🔤 Gemini를 이용해 이미지 검색용 영어 쿼리 생성
def generate_image_search_query(user_input: str) -> str:
    prompt = (
        "사용자의 여행 관련 질문을 이미지 검색용 영어 쿼리로 바꿔줘. "
        "짧고 명확한 명사 형태의 표현으로. 예: '서울의 맛집' → 'Seoul street food' 와 같은 식으로.\n\n"
        f"입력: {user_input}\n영어 쿼리:"
    )
    response = gemini.generate_content(prompt)
    return response.text.strip().strip('"')

# 🖼️ Pexels에서 이미지 검색
def get_pexels_image(query: str, access_key: str) -> str:
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": access_key}
    params = {"query": query, "per_page": 1, "orientation": "landscape"}
    res = requests.get(url, headers=headers, params=params)

    if res.status_code == 200:
        data = res.json()
        if data['photos']:
            return data['photos'][0]['src']['medium']
    return None

# 🎯 전체 통합 함수
def get_image_for_input(user_input: str) -> str:
    english_query = generate_image_search_query(user_input)
    print(f"🔍 영어 쿼리: {english_query}")
    image_url = get_pexels_image(english_query, PEXELS_API_KEY)
    return image_url

# ▶ 테스트 실행
if __name__ == "__main__":
    user_input = input("이미지로 표현하고 싶은 여행 문장을 입력하세요: ").strip()
    image_url = get_image_for_input(user_input)
    if image_url:
        print(f"📷 이미지 URL: {image_url}")
    else:
        print("❌ 관련 이미지를 찾지 못했습니다.")
