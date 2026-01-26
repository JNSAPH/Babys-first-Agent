from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
from operator import add

class State(TypedDict):
    messages: Annotated[List[BaseMessage], add]  # Chat history
    research: str  # Research data
    summary: str  # Final summary