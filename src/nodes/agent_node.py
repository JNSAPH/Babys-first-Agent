import logging
from src.agent.state import State
from src.agent.model import agent

logger = logging.getLogger(__name__)

def agent_node(state: State) -> dict:
    """
    Agent node that generates responses using the language model.
    Takes the conversation history and generates the next message.
    """
    logger.info("> Invoking Agent Node")
    logger.info(f"  Message count: {len(state['messages'])}")
    
    # Log last few messages for context
    for i, msg in enumerate(state["messages"][-3:]):
        msg_type = type(msg).__name__
        content_preview = str(msg.content)[:100] if hasattr(msg, 'content') else "N/A"
        tool_calls = getattr(msg, 'tool_calls', [])
        logger.info(f"  Message[-{len(state['messages'][-3:])-i}]: {msg_type} | Tools: {len(tool_calls)} | Content: {content_preview}")
        
    result = agent.invoke({"messages": state["messages"]})  # Input format for create_agent
    
    # Log what the agent decided to do
    result_messages = result.get("messages", [])
    if result_messages:
        last_result = result_messages[-1]
        has_tool_calls = hasattr(last_result, 'tool_calls') and last_result.tool_calls
        logger.info(f"  Agent output: {type(last_result).__name__} with {len(getattr(last_result, 'tool_calls', []))} tool calls")
        if has_tool_calls:
            for tc in last_result.tool_calls:
                logger.info(f"    → Tool call: {tc['name']} with args {tc['args']}")
    
    logger.info("  Structured response: %s", result.get("structured_response"))

    return result