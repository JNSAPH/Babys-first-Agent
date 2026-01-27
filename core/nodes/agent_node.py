import logging
from core.state import State
from core.model import agent

logger = logging.getLogger(__name__)

def agent_node(state: State) -> dict:
    """
    Agent node that generates responses using the language model.
    Takes the conversation history and generates the next message.
    """
    logger.debug("> Invoking Agent Node")
        
    result = agent.invoke({"messages": state["messages"]})  # Input format for create_agent
    
    logger.debug("Structured response: %s", result.get("structured_response"))
    # logger.debug("LLM Output: %s", result)

    return result