import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from router import router

# Initialize FastAPI
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/AgenticChatbot/v1", tags=["Agentic Chatbot"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)