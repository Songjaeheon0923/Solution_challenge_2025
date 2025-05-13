import os
import faiss
import numpy as np
import re
import json
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from typing import List
from google.generativeai import configure, GenerativeModel

# ✅ 환경변수 로드
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY가 .env에 설정되어 있지 않습니다.")

# ✅ Gemini API 설정
configure(api_key=api_key)
gemini_model = GenerativeModel("models/gemini-1.5-flash")

# ✅ 임베딩 모델 로드
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ✅ 설정
INDEX_ROOT = "embeddings"
CATEGORIES = ["contents", "historical", "preparation"]

# ✅ 질문 임베딩
def embed_query(text: str) -> np.ndarray:
    embedding = model.encode([text])[0]
    return np.array([embedding], dtype=np.float32)

# ✅ 유사 문서 검색
def search_similar_docs(query: str, category: str, top_k: int = 3) -> List[str]:
    index_path = os.path.join(INDEX_ROOT, f"{category}.index")
    path_txt = os.path.join(INDEX_ROOT, f"{category}_paths.txt")

    if not os.path.exists(index_path) or not os.path.exists(path_txt):
        raise FileNotFoundError(f"{category} 인덱스가 존재하지 않음")

    index = faiss.read_index(index_path)
    with open(path_txt, "r", encoding="utf-8") as f:
        id_map = [line.strip() for line in f.readlines()]

    query_vec = embed_query(query)
    distances, indices = index.search(query_vec, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(id_map):
            with open(id_map[idx], "r", encoding="utf-8") as f:
                results.append(f.read().strip())

    return results

# ✅ 질문 분류
def classify_question_with_gemini(question: str) -> str:
    prompt = (
        "다음 문장이 여행에 대한 어떤 유형인지 분류해 주세요. "
        "만약, 질문에 문화, 역사와 같은 단어가 들어가면 historical로 분류될 가능성이 큽니다. "
        "만약, 질문에 음식, 할 것, 즐길거리, 명소, 풍경과 같은 단어가 들어가면 contents로 분류될 가능성이 큽니다. "
        "만약, 질문에 준비할 것, 필요한 것, 준비물과 같은 단어가 들어가면 preparation로 분류될 가능성이 큽니다. "
        "다음 중 하나만 답변하세요: contents, historical, preparation\n\n"
        f"문장: {question}"
    )
    response = gemini_model.generate_content(prompt)
    category = response.text.strip().lower()

    if category not in CATEGORIES:
        raise ValueError(f"잘못된 카테고리 반환됨: {category}")
    return category

# ✅ 답변 생성
def generate_answer_with_gemini(question: str, docs: List[str]) -> str:
    context = "\n---\n".join(docs)
    full_prompt = (
        "당신은 여행 도우미입니다. 아래 문서를 참고하여 사용자의 질문에 친절하고 유용하게 답변하세요.\n"

        f"[사용자 질문]\n{question}\n\n"
        f"[참고 문서]\n{context}"
    )
    response = gemini_model.generate_content(full_prompt)
    return response.text.strip()

# ✅ 요약 생성 (수정 금지)
def generate_summary_with_gemini(answer: str) -> str:
    prompt = (
        "당신은 여행 도우미입니다. 다음 내용을 요약해서 1~3문장으로 만들어주세요. "
        "응답은 마크다운 없이 일반 문장으로 구성하고, 해당 지역의 특성을 예시와 함께 포함해주세요.\n\n"
        f"내용: {answer}"
    )
    response = gemini_model.generate_content(prompt)
    return response.text.strip()

def clean_markdown(text: str) -> str:
    return text.replace("*", "").strip()


import json
import re

# 🔧 마크다운 코드블럭(```json ... ```)만 제거
def clean_code_block_json(text: str) -> str:
    return re.sub(r"^```json\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE | re.DOTALL)

# 🔧 *만 제거 (historical용)
def clean_markdown(text: str) -> str:
    return text.replace("*", "").strip()

# ✅ message 구조화 함수
def format_message(category: str, answer: str) -> dict | str:
    if category == "historical":
        prompt = (
            "다음 내용을 시대별로 정리해서 JSON 형식으로 출력해줘. 각 시대는 해당 지역에서만 사용하는 고유 시대명이면 좋아. 각 시대는 다음과 같은 구조로 표현해야 해:\n\n"
            "{\n"
            "  \"[시대 이름]\": {\n"
            "    \"시대 설명\": \"해당 지역의 당대 역사적 배경에 대한 2~3문장의 설명\",\n"
            "    \"주요 사건\": [\n"
            "      {\"이름\": \"사건명\", \"설명\": \"그 사건이 왜 중요한지에 대한 설명\"},\n"
            "      ... (최소 2개)\n"
            "    ]\n"
            "  },\n"
            "  ...\n"
            "}\n\n"
            "조건:\n"
            "- 마크다운 없이 JSON만 출력\n"
            "- 각 시대별로 반드시 '시대 설명'과 2개 이상의 '주요 사건' 포함\n"
            "- 사건 이름은 간결하게, 설명은 2문장 이상\n\n"
            f"내용:\n{answer}"
        )
        response = gemini_model.generate_content(prompt)
        try:
            cleaned = clean_code_block_json(response.text)
            return json.loads(cleaned)
        except json.JSONDecodeError:
            print("❌ JSON 파싱 오류 (historical):\n", response.text)
            raise



    elif category == "contents":
        prompt = (
            "다음 내용을 JSON 형식으로 변환해줘. 각 항목은 최소 2개 이상 포함하고, 마크다운 없이 JSON만 출력해. "
            "각 항목은 name과 information 필드를 포함하고 imageurl은 제외해. "
            "**information은 두 문장 이상으로 구성된 상세 설명이어야 해.**"
            "형식은 다음과 같아:\n"
            "{\n"
            "  \"Place\": [ {\"name\": \"...\", \"information\": \"...\"}, ... ],\n"
            "  \"F&B\": [ {\"name\": \"...\", \"information\": \"...\"}, ... ],\n"
            "  \"Activity\": [ {\"name\": \"...\", \"information\": \"...\"}, ... ]\n"
            "}\n"
            f"\n내용:\n{answer}"
        )
        response = gemini_model.generate_content(prompt)
        try:
            cleaned = clean_code_block_json(response.text)
            return json.loads(cleaned)
        except json.JSONDecodeError:
            print("❌ JSON 파싱 오류 (contents):\n", response.text)
            raise

    elif category == "preparation":
        prompt = (
            "다음 내용을 JSON 형식으로 변환해줘. Clothes와 ETC 항목 각각 최소 2개 이상 포함하고, "
            "각 항목은 name과 information 필드를 포함해. imageurl은 제외하고 마크다운 없이 JSON만 출력해."
            "**information은 두 문장 이상으로 구성된 상세 설명이어야 해.**"
            "형식은 다음과 같아:\n"
            "{\n"
            "  \"Clothes\": [ {\"name\": \"...\", \"information\": \"...\"}, ... ],\n"
            "  \"ETC\": [ {\"name\": \"...\", \"information\": \"...\"}, ... ]\n"
            "}\n"
            f"\n내용:\n{answer}"
        )
        response = gemini_model.generate_content(prompt)
        try:
            cleaned = clean_code_block_json(response.text)
            return json.loads(cleaned)
        except json.JSONDecodeError:
            print("❌ JSON 파싱 오류 (preparation):\n", response.text)
            raise

    else:
        raise ValueError(f"알 수 없는 카테고리: {category}")


# ✅ 전체 처리
def handle_full_response(question: str) -> dict:
    category = classify_question_with_gemini(question)
    print(f"🧭 분류된 카테고리: {category}")
    docs = search_similar_docs(question, category)
    answer = generate_answer_with_gemini(question, docs)
    message = format_message(category, answer)
    summary = generate_summary_with_gemini(answer)
    return {
        "category": category,
        "message": message,
        "summary": summary
    }

# ✅ 테스트 실행
if __name__ == "__main__":
    question = input("여행 관련 질문을 입력하세요: ").strip()
    result = handle_full_response(question)
    print("\n📌 전체 결과:\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
