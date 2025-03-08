import os
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import scrolledtext
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from langchain.tools import tool
from langchain.agents import Tool
import datetime

# Set API Keys
os.environ["GROQ_API_KEY"] = "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"
os.environ["TAVILY_API_KEY"] = "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"

# Initialize Language Model
llm = init_chat_model("llama3-70b-8192", model_provider="groq")

# Chatbot Instructions
prompt = (
    "You are a Personal assistant named Jay developed by Debjyoti. You are an expert in Engineering, Technology, Physics, Astronomy, and Cosmology."
    "You are highly interactive, intelligent, and proactive in assisting users with their queries."
    "Provide detailed and engaging responses while maintaining an expert and futuristic tone."
    "Use the tools provided to give up-to-date responses."
)

# Web Search Tool
search_tool = TavilySearchResults(
    name="tavily_search_engine",
    description="A search engine optimized for retrieving information from the web.",
    max_results=2,
)

# Calculator Tool
@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression and returns the result."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"
    
# Define a very simple tool function that returns the current time
def get_current_time(*args, **kwargs):
    """Returns the current time in H:MM AM/PM format."""
    import datetime  # Import datetime module to get current time

    now = datetime.datetime.now()  # Get current time
    return now.strftime("%I:%M %p")  # Format time in H:MM AM/PM format

def get_current_date(*args, **kwargs):
    """Returns the current date in YYYY-MM-DD format."""
    return datetime.datetime.now().strftime("%Y-%m-%d")

# Register Tools
tools = [
    Tool(
        name="Web Search",
        func=search_tool.invoke,
        description="Useful for retrieving the latest information from the web.",
    ),
    Tool(
        name="Calculator",
        func=calculator,
        description="Useful for performing mathematical calculations.",
    ),
    Tool(
        name="Time",  # Name of the tool
        func=get_current_time,  # Function that the tool will execute
        # Description of the tool
        description="Useful for when you need to know the current time",
    ),
    Tool(
        name="Wikipedia",
        func=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()).run,
        description="Fetches information from Wikipedia.",
    ),
    Tool(
        name="Current Date",
        func=get_current_date,
        description="Provides the current date in YYYY-MM-DD format.",
    ),
]

# Conversational Memory
memory = MemorySaver()

# Define Chatbot Function
def agenticchatbot(query, threadid):
    """Handles AI chatbot response with LangChain agents."""
    try:
        agent = create_react_agent(llm, tools, prompt=prompt, checkpointer=memory)
        config = {"configurable": {"thread_id": threadid}}
        response = agent.invoke({"messages": [HumanMessage(query)]}, config)
        final_output = response["messages"][-1].content
        return final_output
    except Exception as e:
        return "I'm experiencing some technical difficulties."

# Speech-to-Text (STT) using Whisper API
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print(f"🗣️ User said: {text}")
        return text
    except Exception as e:
        print("❌ Error recognizing speech:", str(e))
        return None

# Text-to-Speech (TTS) using pyttsx3
def speak_response(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)  # Speech speed
    engine.setProperty("volume", 1.0)
    engine.say(text)
    engine.runAndWait()

# Voice-Controlled Chatbot Loop with Exit and Typing Option
def voice_chatbot():
    """Runs a voice-controlled chatbot session."""
    while True:
        print("\n🎤 Say something or type your query:")
        # user_input = recognize_speech()
        user_input = input("📝 Type your query: ")

        if user_input in ["exit", "quit"]:
            print("👋 Goodbye! Exiting Jay Assistant.")
            speak_response("Goodbye! Have a great day!")
            break  # Exit the loop

        # if not user_input:
        #     user_input = input("📝 Type your query: ")  # Allow typing if speech fails

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye! Exiting Jay Assistant.")
            speak_response("Goodbye! Have a great day!")
            break  # Exit the loop

        response = agenticchatbot(user_input, threadid="12345")
        print(f"🤖 Jay: {response}")
        # speak_response(response)

#  Do you want to add voice wake word like "Hey Jay"?

# Run the Voice Assistant
# if __name__ == "__main__":
#     voice_chatbot()
