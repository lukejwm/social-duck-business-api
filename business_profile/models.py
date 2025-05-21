from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class BusinessUser(Base):
    __tablename__ = "business_user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    business_name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    town_city = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)

    chats = relationship("ChatHistory", back_populates="business")


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False)

    chats = relationship("ChatHistory", back_populates="user")
    

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    username = Column(String(100))
    business_id = Column(Integer, ForeignKey("business_user.id"))
    title = Column(String(75))
    body = Column(Text)
    star_rating = Column(Integer)
    review_type = Column(Enum("Positive", "Negative"))
    alert_seen = Column(Boolean, default=False)

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    business_id = Column(Integer, ForeignKey("business_user.id"))
    business_email = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    user_email = Column(String)
    message = Column(String)
    sender = Column(String)
    receiver = Column(String)
    timestamp = Column(DateTime, default=datetime.today)
    business = relationship("BusinessUser", back_populates="chats")
    user = relationship("User", back_populates="chats")
