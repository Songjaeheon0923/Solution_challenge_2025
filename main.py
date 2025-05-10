import os
import faiss
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from typing import List
from google.generativeai import configure, GenerativeModel

# ✅ .env에서 환경변수 로드
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY가 .env에 설정되어 있지 않습니다.")

# ✅ Gemini API 설정
configure(api_key=api_key)
gemini_model = GenerativeModel("models/gemini-1.5-flash")

# ✅ 로컬 임베딩 모델 로드
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# 🔧 경로 설정
INDEX_ROOT = "embeddings"
DOC_ROOT = "docs"
CATEGORIES = ["contents", "historical", "preparation"]

# 🔍 질문을 벡터로 변환
def embed_query(text: str) -> np.ndarray:
    embedding = model.encode([text])[0]
    return np.array([embedding], dtype=np.float32)

# 🔎 카테고리에서 유사 문서 검색
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

# 🔮 Gemini API를 사용해 질문 분류
def classify_question_with_gemini(question: str) -> str:
    prompt = (
        "다음 문장이 여행에 대한 어떤 유형인지 분류해 주세요. "
        "만약, 질문에 문화, 역사와 같은 단어가 들어가면 historical로 분류될 가능성이 큽니다."
        "만약, 질문에 음식, 할 것, 즐길거리, 명소, 풍경과 같은 단어가 들어가면 contents로 분류될 가능성이 큽니다."
        "만약, 질문에 준비할 것, 필요한 것, 준비물과 가은 단어가 들어가면, preparation로 분류될 가능성이 큽니다."
        "다음 중 하나만 답변하세요: contents, historical, preparation\n\n"
        f"문장: {question}"
    )
    response = gemini_model.generate_content(prompt)
    category = response.text.strip().lower()

    if category not in CATEGORIES:
        raise ValueError(f"잘못된 카테고리 반환됨: {category}")
    return category

# 💬 Gemini 응답 생성
def generate_answer_with_gemini(question: str, docs: List[str]) -> str:
    context = "\n---\n".join(docs)
    full_prompt = (
        "당신은 여행 도우미입니다. 아래 문서를 참고하여 사용자의 질문에 친절하고 유용하게 답변하세요.\n\n"
        f"[사용자 질문]\n{question}\n\n"
        f"[참고 문서]\n{context}"
    )
    response = gemini_model.generate_content(full_prompt)
    return response.text.strip()

# 🧠 전체 흐름
def handle_query(question: str) -> str:
    category = classify_question_with_gemini(question)
    print(f"🧭 분류된 카테고리: {category}")
    docs = search_similar_docs(question, category)
    answer = generate_answer_with_gemini(question, docs)
    return answer

# 🟢 테스트 실행
if __name__ == "__main__":
    question = input("여행 관련 질문을 입력하세요: ").strip()
    result = handle_query(question)
    print("\n📌 최종 답변:\n")
    print(result)
