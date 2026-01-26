import logging
from core.state import State

logger = logging.getLogger(__name__)

def summarize_node(state: State) -> dict:
    """
    Summarize the conversation and research into a concise output.
    Combines research data with message contents.
    """
    # Extract content from all messages
    logger.debug("> Summarizing conversation and research data")

    message_contents = [
        msg.content for msg in state["messages"]
        if hasattr(msg, "content") and msg.content
    ]
    
    # Combine research and messages
    all_content = [state["research"]] if state["research"] else []
    all_content.extend(message_contents)
    
    full_text = "\n".join(all_content)
    
    # Truncate if too long
    if len(full_text) > 200:
        summary = full_text[:200] + "..."
    else:
        summary = full_text
    
    return {"summary": summary}