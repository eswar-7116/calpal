from pydantic import BaseModel


class ChatRequest(BaseModel):
    chat: str
