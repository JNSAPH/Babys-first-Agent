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
    
    # This currently only appends the System Message to the messages list. Meaning that the SystemMessage will come after
    # the HumanMessage in the conversation history. This is NOT A GOOD WAY TO DO IT. In Production we will remove this Node entirely
    # and instead prepend the SystemMessage to the messages list before passing it to the LLM. AKA. Have it in the invoke call.
    
    return {
        "messages": [SystemMessage(content=StrSystemMessage)]
    }