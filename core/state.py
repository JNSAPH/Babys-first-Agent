from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field
from operator import add

class FinalResponse(BaseModel):
    """Final agent response with summary and action taken."""
    summary: str = Field(..., description="One-sentence summary")
    weather: str | None = Field(None, description="Weather info if retrieved")
    file_written: bool = Field(default=False, description="File written?")
    thoughts: str = Field(..., description="Agent's final thoughts about what it did, why it called certain tools, and if it called a tool multiple times, why.")

class State(TypedDict):
    messages: Annotated[List[BaseMessage], add]  # Chat history
    research: str  # Research data
    summary: str  # Final summary
    used_tokens: int  # Total tokens used
    structured_response: FinalResponse | None  # Agent's structured output
