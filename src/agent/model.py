import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from src.tools import write_text_file_tool, get_weather_tool
from src.agent.state import FinalResponse
from langchain.agents import create_agent 

load_dotenv()

tools = [write_text_file_tool, get_weather_tool]

model = ChatOpenAI(
    temperature=0,
    model_name="gpt-5-nano",
).bind_tools(tools)


agent = create_agent(
    model=model,
    tools=tools,              # redundant but fine
    response_format=FinalResponse
)