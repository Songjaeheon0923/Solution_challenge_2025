from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import handle_full_response
from scrape_picture import get_image_for_input

app = FastAPI()

# ✅ 요청 스키마
class QueryRequest(BaseModel):
    question: str

# ✅ 응답 스키마
class QueryResponse(BaseModel):
    response: dict

# ✅ message 내부 항목에 이미지 URL 삽입
def enrich_message_with_images(message: dict, category: str) -> dict:
    if category == "contents":
        for section in ["Place", "F&B", "Activity"]:
            for item in message.get(section, []):
                image_url = get_image_for_input(item["name"])
                item["imageurl"] = image_url

    elif category == "preparation":
        for section in ["Clothes", "ETC"]:
            for item in message.get(section, []):
                image_url = get_image_for_input(item["name"])
                item["imageurl"] = image_url

    return message

# ✅ 메인 API 라우터
@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    question = request.question
    try:
        # 핵심 응답 생성
        core = handle_full_response(question)
        category = core["category"]

        # 이미지 처리 분기
        if category in ["contents", "preparation"]:
            core["message"] = enrich_message_with_images(core["message"], category)
            image_url = None  # 대표 이미지 없음
        elif category == "historical":
            image_url = get_image_for_input(question)
        else:
            image_url = None

        return {
            "response": {
                **core,
                "imageurl": image_url
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ 루트 확인용
@app.get("/")
def root():
    return {"message": "여행 도우미 API입니다. POST /ask로 질문을 보내보세요."}
