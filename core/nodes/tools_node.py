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


from langchain_core.messages import AIMessage, ToolMessage
# from core.state import State
# from core.model import tools
# import logging

# logger = logging.getLogger(__name__)

# # Automatically build tool map from the tools list (user-defined tools only)
# TOOL_MAP = {tool.name: tool for tool in tools}

# def tools_node(state: State) -> dict:
#     """
#     Execute REAL tool calls from agent (skips structured output like FinalResponse).
    
#     1. Filters out structured output tool calls (FinalResponse)
#     2. Executes only user-defined tools (weather, file_writer)
#     3. Returns ToolMessages for executed tools only
#     """
#     logger.debug("> Processing agent tool calls")
#     last_msg = state["messages"][-1]
    
#     # Early exit: No tool calls
#     if not isinstance(last_msg, AIMessage) or not last_msg.tool_calls:
#         logger.debug("No tool calls → pass through")
#         return {"messages": []}
    
#     # STEP 1: Filter OUT structured output tools (prevents loops)
#     all_tool_calls = last_msg.tool_calls
#     real_tool_calls = [
#         tc for tc in all_tool_calls 
#         if tc["name"] not in ["FinalResponse"]  # Skip structured output
#     ]
    
#     logger.debug("All calls: %s | Real tools: %s", 
#                 [tc["name"] for tc in all_tool_calls],
#                 [tc["name"] for tc in real_tool_calls])
    
#     # STEP 2: Early exit if only structured output (route_agent will summarize)
#     if not real_tool_calls:
#         logger.debug("Only structured output → skip execution")
#         return {"messages": []}
    
#     # STEP 3: Execute REAL tools only
#     tool_results = []
#     for tool_call in real_tool_calls:  # FIXED: real_tool_calls, not all_tool_calls
#         tool_name = tool_call["name"]
#         tool_args = tool_call["args"]
        
#         logger.debug(f"> Running '{tool_name}'({tool_args})")
        
#         tool_func = TOOL_MAP.get(tool_name)
#         if tool_func:
#             try:
#                 result = tool_func.invoke(tool_args)
#                 tool_results.append(ToolMessage(
#                     content=result, 
#                     tool_call_id=tool_call["id"]
#                 ))
#                 logger.debug(f"> '{tool_name}' SUCCESS")
#             except Exception as e:
#                 logger.error(f"> '{tool_name}' ERROR: {e}")
#                 tool_results.append(ToolMessage(
#                     content=f"ERROR: {str(e)}", 
#                     tool_call_id=tool_call["id"]
#                 ))
#         else:
#             logger.warning(f"> Unknown tool: '{tool_name}'")
#             tool_results.append(ToolMessage(
#                 content=f"ERROR: Unknown tool '{tool_name}'", 
#                 tool_call_id=tool_call["id"]
#             ))
    
#     return {"messages": tool_results}  # Only real tool results


# def route_agent(state: State) -> str:
#     """
#     Route the agent's response to either tools or summarization.
#     Checks if the agent requested tool calls. If so route to tools, else to summarize.
#     """
#     # Find latest MEssage from the LLM
#     messages = state["messages"]

#     # Find LAST AIMessage (ignore trailing ToolMessages)
#     ai_messages = [m for m in reversed(messages) if isinstance(m, AIMessage)]
#     last_ai = ai_messages[0] if ai_messages else None
    
#     if not last_ai:
#         logger.warning("No AIMessage found → summarize")
#         return "summarize"
    
#     tool_calls = last_ai.tool_calls or []
#     logger.debug("Calling Tools: %s", tool_calls)

#     # Check if the only tool call is FinalResponse - if so, go directly to summarize
#     if len(tool_calls) == 1 and tool_calls[0].get("name") == "FinalResponse":
#         logger.debug("FinalResponse detected → summarize")
#         return "summarize"
    
#     if tool_calls:  # Agent wants more tools
#         return "tools"
#     return "summarize"  # Agent finished


