from pydantic import BaseModel

class BusinessInfo(BaseModel):
    email: str
    business_name: str
    address: str
    town_city: str
    type: str

class BusinessUserResponse(BaseModel):
    id: int
    email: str
    business_name: str
    address: str
    town_city: str
    type: str

    class Config:
        orm_mode = True

class SendMessageRequest(BaseModel):
    session_id: str
    message: str

class FeedbackResponse(BaseModel):
    username: str
    title: str
    body: str
    star_rating: int

    class Config:
        orm_mode = True

class StartChatRequest(BaseModel):
    business_email: str
    user_email: str
    message: str


class ChatHistory(BaseModel):
    session_id: str
    business_id: int
    business_email: str
    user_id: int
    user_email: str
    message: str
    sender: str
    receiver: str

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True
