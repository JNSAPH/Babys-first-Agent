import logging
from src.agent.state import State

logger = logging.getLogger(__name__)

def output_node(state: State) -> dict:
    """
    Summarize the conversation and research into a concise output.
    Combines research data with message contents.
    """
    # Extract content from all messages
    logger.info("> OUTPUT NODE: Creating final output")
    logger.info(f"  Total messages: {len(state['messages'])}")

    message_contents = []
    for msg in state["messages"]:
        if hasattr(msg, "content") and msg.content:
            # Handle both string and list content
            if isinstance(msg.content, str):
                message_contents.append(msg.content)
            elif isinstance(msg.content, list):
                # Convert list content to string (common in some message types)
                logger.info(f"  Converting list content from {type(msg).__name__}")
                message_contents.append(str(msg.content))
    
    logger.info(f"  Messages with content: {len(message_contents)}")
    
    # Combine research and messages
    research = state.get("research", "")
    all_content = [research] if research else []
    all_content.extend(message_contents)
    
    full_text = "\n".join(all_content)
    
    logger.info(f"  Combined text length: {len(full_text)} chars")
    
    # Truncate if too long
    if len(full_text) > 200:
        summary = full_text[:200] + "..."
        logger.info("  Summary truncated to 200 chars")
    else:
        summary = full_text
    
    logger.info(f"  Final summary: {summary[:50]}...")
    return state