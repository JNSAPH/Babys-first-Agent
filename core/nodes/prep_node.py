import logging
from core.state import State
from core.messages.messages import StrSystemMessage
from langchain_core.messages import SystemMessage

logger = logging.getLogger(__name__)

def prep_node(state: State) -> dict:
    """
    Prepare the conversation with a system prompt.
    Initializes the agent with instructions and guidelines.
    """
    logger.debug("> Preparing conversation with system prompt")
    logger.debug(f"System message content length: {len(StrSystemMessage)} characters")
    
    return {
        "messages": [SystemMessage(content=StrSystemMessage)]
    }