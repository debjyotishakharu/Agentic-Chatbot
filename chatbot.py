import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.tools import tool
from langchain.agents import Tool
# import asyncio


os.environ["GROQ_API_KEY"] = "your key here"
os.environ["TAVILY_API_KEY"] = "your key here"

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
    
tools = [
            Tool(
                name="Web Search",
                func=search_tool.invoke,
                description="Useful for retrieving the latest information from the web."
            ),
            Tool(
                name="Calculator",
                func=calculator,
                description="Useful for performing mathematical calculations."
            )
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

    
    