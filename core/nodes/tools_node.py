from langchain_core.messages import AIMessage, ToolMessage
from core.state import State
from core.model import tools
import logging

logger = logging.getLogger(__name__)

# Automatically build tool map from the tools list
TOOL_MAP = {tool.name: tool for tool in tools}

def tools_node(state: State) -> dict:
    """
    Execute tool calls requested by the agent.
    Processes the last AI message and executes any tool calls it contains.
    """
    logger.debug("> Executing tool calls from agent message")
    last_msg = state["messages"][-1]
    
    if not isinstance(last_msg, AIMessage) or not last_msg.tool_calls:
        return {"messages": state["messages"]}
    
    tool_results = []
    for tool_call in last_msg.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        logger.debug(f"> Executing tool '{tool_name}' with args {tool_args}")
        
        # Get the actual tool function and execute it
        tool_func = TOOL_MAP.get(tool_name)

        if tool_func:
            try:
                # Execute the tool and capture the result
                result = tool_func.invoke(tool_args)
                tool_results.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
            except Exception as e:
                # Log the error and append an error message
                logger.error(f"> Tool '{tool_name}' failed: {e}")
                tool_results.append(ToolMessage(content=f"ERROR: {str(e)}", tool_call_id=tool_call["id"]))
        else:
            # Log unknown tool and append an error message
            logger.warning(f"> Unknown tool: {tool_name}")
            tool_results.append(ToolMessage(content=f"ERROR: Unknown tool '{tool_name}'", tool_call_id=tool_call["id"]))
    
    return {"messages": tool_results}


def route_agent(state: State) -> str:
    """
    Route the agent's response to either tools or summarization.
    Checks if the agent requested tool calls.
    """
    last = state["messages"][-1]
    tool_calls = getattr(last, "tool_calls", [])
    logger.debug(f"> Routing agent response based on tool calls in message: {tool_calls}")
    
    # If the last message is from the AI and contains tool calls, route to tools
    if isinstance(last, AIMessage) and last.tool_calls:
        return "tools"
    
    # Otherwise, proceed to summarization
    return "summarize"
