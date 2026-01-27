import logging
from langchain_core.messages import AIMessage
from core.state import State

logger = logging.getLogger(__name__)

def token_node(state: State) -> dict:
    total = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
    for msg in state["messages"]:
        if isinstance(msg, AIMessage):
            metadata = msg.response_metadata or {}
            print(f"Message metadata: {metadata}")

    print(f"Total tokens used so far: {total}")

    return {"used_tokens": total}