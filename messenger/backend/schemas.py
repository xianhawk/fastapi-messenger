import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str
    
    
class UserLogin(BaseModel):
    email: str
    password: str


class Message(BaseModel):
    text: str
    sender_id: int
    recipient_id: int
    
    class Config:
        orm_mode = True


class MessageGet(BaseModel):
    recipient_id: int


class MessageSend(BaseModel):
    text: str
    recipient_id: int


class User(UserBase):
    id: int
    messages: list[Message] = []

    class Config:
        orm_mode = True


class ContactSearch(BaseModel):
    email: str    


class Contact(BaseModel):
    contact_user_id: int
    date_of_addition: datetime.datetime
    
    class Config:
        orm_mode = True


class ContactAdd(BaseModel):
    contact_user_id: int
