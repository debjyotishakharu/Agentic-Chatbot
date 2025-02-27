from fastapi import HTTPException, UploadFile, File, APIRouter, Form
from chatbot import agenticchatbot

router = APIRouter()

@router.post("/agentic_chatbot")
def agentic_chatbot(query: str = Form(...),threadID: str = Form("1")):
    try:
        print("Inside Router")
        response=agenticchatbot(query,threadID)
        print("response", response)
        return response
    except Exception as e:
        print("failed at agentic_chatbot router")
        print(str(e))
        raise HTTPException(**e.__dict__)