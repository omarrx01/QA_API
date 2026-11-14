
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from api.database import Base, engine, get_db
from api.models import QuestionAnswer
from api.schemas import QuestionAnswerCreate, QuestionAnswerResponse
from api.cache import get_cached_answer, cache_answer


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Q&A API", lifespan=lifespan)


@app.get("/")
def home():
    return {"message": "Q&A API is running"}


@app.post("/questions", response_model=QuestionAnswerResponse, status_code=201)
def create_question(data: QuestionAnswerCreate, db: Session = Depends(get_db)):
    record = QuestionAnswer(
        question=data.question,
        answer=data.answer
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    cache_answer(record.question.strip().lower(), record.answer)
    return record

  
@app.get("/questions/{question_id}", response_model=QuestionAnswerResponse)
def get_question(question_id: str, db: Session = Depends(get_db)):
    record = db.query(QuestionAnswer).filter(
        QuestionAnswer.id == question_id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Question not found")

    return record



from sqlalchemy import func

@app.get("/answers")
def get_answer(question: str, db: Session = Depends(get_db)):
    normalized_question = question.strip().lower()

    cached = get_cached_answer(normalized_question)

    if cached is not None:
        return {"answer": cached, "source": "redis"}

    record = db.query(QuestionAnswer).filter(
        func.lower(QuestionAnswer.question) == normalized_question
    ).order_by(QuestionAnswer.created_at.desc()).first()

    if not record:
        raise HTTPException(status_code=404, detail="Answer not found")

    cache_answer(normalized_question, record.answer)

    return {"answer": record.answer, "source": "postgresql"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}