from langchain_openai import ChatOpenAI
from core.tools import write_text_file_tool, get_weather_tool

tools = [write_text_file_tool, get_weather_tool]

model = ChatOpenAI(
    temperature=0,
    model_name="gpt-5-nano",
).bind_tools(tools)