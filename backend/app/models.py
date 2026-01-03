from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str

class Message(BaseModel):
    recipient: str
    content: str
