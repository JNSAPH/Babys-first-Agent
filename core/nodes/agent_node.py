import logging
from core.state import State
from core.model import model

logger = logging.getLogger(__name__)

def agent_node(state: State) -> dict:
    """
    Agent node that generates responses using the language model.
    Takes the conversation history and generates the next message.
    """
    logger.debug("> Invoking agent model")

    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}