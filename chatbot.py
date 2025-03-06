import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from langchain.chains import ConversationalRetrievalChain
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.memory import ConversationBufferMemory
from langchain.tools import tool
from langchain.agents import Tool
import datetime
# import asyncio

os.environ["GROQ_API_KEY"] = "Your_key_here"
os.environ["TAVILY_API_KEY"] = "Your_key_here"

llm = init_chat_model("llama3-70b-8192", model_provider="groq")

prompt = (
    "You are a Personal assistant named Jay. You are an expert in Engineering, Technology, Physics, Astronomy and Cosmology."
    "You are highly interactive, intelligent, and proactive in assisting users with their queries."
    "Provide detailed and engaging responses while maintaining an expert and futuristic tone."
    "Use the tools provided to give up to date responses"
)

search_tool = TavilySearchResults(
  name="tavily_search_engine",
  description="A search engine optimized for retrieving information from web based on user query.",
  max_results=2,)

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

memory = MemorySaver()

def agenticchatbot(query, threadid):
    try:
        agent = create_react_agent(llm, tools, prompt=prompt, checkpointer=memory)
        config={"configurable": {"thread_id": threadid}}
        response=agent.invoke(
        {"messages": [HumanMessage(query)]},
        config,)
        print(response)
        final_output=response["messages"][-1].content
        print(final_output)
        return final_output
    except Exception as e:
        print("Failed at agentic chatbot:", str(e))
        return "I'm experiencing some technical difficulties."

    
    