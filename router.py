from fastapi import HTTPException, UploadFile, File, APIRouter, Form
from chatbot import agenticchatbot
from pydantic import BaseModel

class ChatbotRequest(BaseModel):
    query: str
    threadID: str = None  # Optional field

router = APIRouter()

@router.post("/agentic_chatbot")
def agentic_chatbot(request: ChatbotRequest):
    try:
        print("Inside Router")
        response=agenticchatbot(request.query,request.threadID)
        print("response", response)
        if isinstance(response, str):  # Ensure response is always JSON
            return {"response": response}
        return response
    except Exception as e:
        print("failed at agentic_chatbot router")
        print(str(e))
        raise HTTPException(**e.__dict__)