from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database import get_db
from . import models, schemas
from uuid import uuid4

router = APIRouter(prefix="/business", tags=["Business"])

@router.post("/register", response_model=schemas.BusinessUserResponse)
def register_business_user(user: schemas.BusinessInfo, db: Session = Depends(get_db)):
    db_user = models.BusinessUser(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/delete/{user_id}")
def delete_business_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.BusinessUser).filter(models.BusinessUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Business user not found")
    db.delete(user)
    db.commit()
    return {"message": "Business user deleted successfully"}

@router.get("/account/{user_id}", response_model=schemas.BusinessUserResponse)
def get_business_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.BusinessUser).filter(models.BusinessUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Business user not found")
    return user

@router.get("/feedback/{business_id}", response_model=list[schemas.FeedbackResponse])
def get_positive_feedback(business_id: int, db: Session = Depends(get_db)):
    feedback = db.query(models.Feedback).filter(
        models.Feedback.business_id == business_id,
        models.Feedback.review_type == "Positive"
    ).all()
    return feedback

@router.get("/feedback/negative/{business_id}")
def get_negative_feedback(business_id: int, db: Session = Depends(get_db)):
    feedback = db.query(models.Feedback, models.User).join(
        models.User, models.Feedback.user_id == models.User.id
    ).filter(
        and_(
            models.Feedback.business_id == business_id,
            models.Feedback.star_rating <= 3
        )
    ).all()

    return [
        {
            "username": user.email,  # Using email as a stand-in for username
            "title": fb.title,
            "body": fb.body,
            "star_rating": fb.star_rating
        } for fb, user in feedback
    ]

@router.post("/chat/start")
def start_chat(chat_data: schemas.StartChatRequest, db: Session = Depends(get_db)):
    business = db.query(models.BusinessUser).filter_by(email=chat_data.business_email).first()
    user = db.query(models.User).filter_by(email=chat_data.user_email).first()
    if not business or not user:
        raise HTTPException(status_code=404, detail="Business or user not found")

    session_id = str(uuid4())
    new_entry = models.ChatHistory(
        session_id=session_id,
        business_id=business.id,
        business_email=business.email,
        user_id=user.id,
        user_email=user.email,
        message=chat_data.message,
        sender=business.email,
        receiver=user.email,
    )
    db.add(new_entry)
    db.commit()
    return {"session_id": session_id, "message": "Chat started"}

@router.post("/chat/send")
def send_message(msg_data: schemas.SendMessageRequest, db: Session = Depends(get_db)):
    chat_session = db.query(models.ChatHistory).filter_by(session_id=msg_data.session_id).first()
    if not chat_session:
        raise HTTPException(status_code=404, detail="Chat session not found")

    new_msg = models.ChatHistory(
        session_id=msg_data.session_id,
        business_id=chat_session.business_id,
        business_email=chat_session.business_email,
        user_id=chat_session.user_id,
        user_email=chat_session.user_email,
        message=msg_data.message,
        sender=chat_session.business_email,
        receiver=chat_session.user_email,
    )
    db.add(new_msg)
    db.commit()
    return {"message": "Message sent"}

@router.get("/chat/{session_id}", response_model=list[schemas.ChatHistory])
def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    history = db.query(models.ChatHistory).filter_by(session_id=session_id).order_by(models.ChatHistory.timestamp).all()
    if not history:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return history
