from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from . import model, schemas
from .database import get_db



app = FastAPI(
    title = "Quiz app", 
    description = "Take your quiz here",
)


@app.post("/question", response_model=schemas.QuizOut, status_code=status.HTTP_201_CREATED)
def create_question(question: schemas.QuizCreate, db: Session = Depends(get_db)):
  try:
    new_question = model.Question(**question.dict())
    print(question.dict())
    print(new_question)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question
  except Exception as e:
    print(str(e))
  


@app.get("/question/{id}",response_model = schemas.QuizOut)
def get_question(id: int, db: Session = Depends(get_db)):
    quest = db.query(model.Question).filter(model.Question.id==id)
    quiz = quest.first()
    if not quiz:
      return HTTPException(status_code=204, detail=f"No question with the id:{id}")
    return quiz

@app.post("/answer/{id}", status_code=status.HTTP_202_ACCEPTED)
def check_answer(id: int, response: schemas.ResponseIn, db: Session = Depends(get_db)):
  quiz = db.query(model.Question).filter(model.Question.id==id).first()
  if quiz.answer.lower() == response.answer.lower(): 
    return {"message": "Correct answer, Move to next question"}
  else:
    return {"message": f"Wrong answer, the correct answer is {quiz.answer}, Move to previous question"}
