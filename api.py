from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import classify_question_with_gemini, handle_query
from scrape_picture import get_image_for_input

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    category: str
    answer: str
    image_url: str | None = None

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    question = request.question
    try:
        category = classify_question_with_gemini(question)
        answer = handle_query(question)
        image_url = None

        if category in ["contents", "historical"]:
            image_url = get_image_for_input(question)

        return QueryResponse(category=category, answer=answer, image_url=image_url)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
