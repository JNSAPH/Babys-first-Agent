import logging

from langsmith import traceable
from src.agent.state import State
from src.agent.messages import StrSystemMessage
from langchain_core.messages import SystemMessage

logger = logging.getLogger(__name__)

@traceable 
def prep_node(state: State) -> dict:
    """
    Prepare the conversation with a system prompt.
    Initializes the agent with instructions and guidelines.
    """
    logger.info("> PREP NODE: Initializing conversation")
    logger.info(f"  System message length: {len(StrSystemMessage)} characters")
    logger.info(f"  Current message count: {len(state.get('messages', []))}")
    
    # This currently only appends the System Message to the messages list. Meaning that the SystemMessage will come after
    # the HumanMessage in the conversation history. This is NOT A GOOD WAY TO DO IT. In Production we will remove this Node entirely
    # and instead prepend the SystemMessage to the messages list before passing it to the LLM. AKA. Have it in the invoke call.
    
    logger.info("  Adding system message to conversation")

    return {
        "messages": [SystemMessage(content=StrSystemMessage)]
    }