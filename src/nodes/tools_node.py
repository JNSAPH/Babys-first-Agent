from langchain_core.messages import AIMessage, ToolMessage
from src.agent.state import State
from src.agent.model import tools
import logging

logger = logging.getLogger(__name__)

# Automatically build tool map from the tools list
TOOL_MAP = {tool.name: tool for tool in tools}

def tools_node(state: State) -> dict:
    """
    Execute tool calls requested by the agent.
    Processes the last AI message and executes any tool calls it contains.
    """
    logger.info("> TOOLS NODE: Executing tool calls from agent message")
    last_msg = state["messages"][-1]
    
    if not isinstance(last_msg, AIMessage) or not last_msg.tool_calls:
        logger.warning("  No tool calls found in last message!")
        return {"messages": state["messages"]}
    
    logger.info(f"  Total tool calls to execute: {len(last_msg.tool_calls)}")
    
    tool_results = []
    for idx, tool_call in enumerate(last_msg.tool_calls, 1):
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        logger.info(f"  [{idx}/{len(last_msg.tool_calls)}] Executing '{tool_name}'")
        logger.info(f"      Args: {tool_args}")
        logger.info(f"      Call ID: {tool_call['id']}")
        
        # Get the actual tool function and execute it
        tool_func = TOOL_MAP.get(tool_name)

        if tool_func:
            try:
                # Execute the tool and capture the result
                result = tool_func.invoke(tool_args)
                result_preview = str(result)[:100]
                logger.info(f"      ✓ Success: {result_preview}")
                tool_results.append(ToolMessage(content=result, tool_call_id=tool_call["id"]))
            except Exception as e:
                # Log the error and append an error message
                logger.error(f"      ✗ FAILED: {e}")
                tool_results.append(ToolMessage(content=f"ERROR: {str(e)}", tool_call_id=tool_call["id"]))
        else:
            # Log unknown tool and append an error message
            logger.warning(f"      ✗ Unknown tool: {tool_name}")
            tool_results.append(ToolMessage(content=f"ERROR: Unknown tool '{tool_name}'", tool_call_id=tool_call["id"]))
    
    logger.info(f"  Completed {len(tool_results)} tool executions")
    return {"messages": tool_results}


def route_agent(state: State) -> str:
    """
    Route the agent's response to either tools or summarization.
    Checks if the agent requested tool calls.
    """
    logger.info("> ROUTING: Determining next step after agent")
    last = state["messages"][-1]
    msg_type = type(last).__name__
    tool_calls = getattr(last, "tool_calls", [])
    
    logger.info(f"  Last message type: {msg_type}")
    logger.info(f"  Tool calls present: {len(tool_calls) > 0}")
    
    if tool_calls:
        logger.info(f"  Found {len(tool_calls)} tool call(s):")
        for tc in tool_calls:
            logger.info(f"    - {tc.get('name', 'unknown')}({tc.get('args', {})})")
    
    # If the last message is from the AI and contains tool calls, route to tools
    if isinstance(last, AIMessage) and last.tool_calls:
        logger.info("  → DECISION: Route to TOOLS")
        return "tools"
    
    # Otherwise, proceed to output
    logger.info("  → DECISION: Route to OUTPUT")
    return "output"


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
#     logger.info("> Processing agent tool calls")
#     last_msg = state["messages"][-1]
    
#     # Early exit: No tool calls
#     if not isinstance(last_msg, AIMessage) or not last_msg.tool_calls:
#         logger.info("No tool calls → pass through")
#         return {"messages": []}
    
#     # STEP 1: Filter OUT structured output tools (prevents loops)
#     all_tool_calls = last_msg.tool_calls
#     real_tool_calls = [
#         tc for tc in all_tool_calls 
#         if tc["name"] not in ["FinalResponse"]  # Skip structured output
#     ]
    
#     logger.info("All calls: %s | Real tools: %s", 
#                 [tc["name"] for tc in all_tool_calls],
#                 [tc["name"] for tc in real_tool_calls])
    
#     # STEP 2: Early exit if only structured output (route_agent will summarize)
#     if not real_tool_calls:
#         logger.info("Only structured output → skip execution")
#         return {"messages": []}
    
#     # STEP 3: Execute REAL tools only
#     tool_results = []
#     for tool_call in real_tool_calls:  # FIXED: real_tool_calls, not all_tool_calls
#         tool_name = tool_call["name"]
#         tool_args = tool_call["args"]
        
#         logger.info(f"> Running '{tool_name}'({tool_args})")
        
#         tool_func = TOOL_MAP.get(tool_name)
#         if tool_func:
#             try:
#                 result = tool_func.invoke(tool_args)
#                 tool_results.append(ToolMessage(
#                     content=result, 
#                     tool_call_id=tool_call["id"]
#                 ))
#                 logger.info(f"> '{tool_name}' SUCCESS")
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
#     logger.info("Calling Tools: %s", tool_calls)

#     # Check if the only tool call is FinalResponse - if so, go directly to summarize
#     if len(tool_calls) == 1 and tool_calls[0].get("name") == "FinalResponse":
#         logger.info("FinalResponse detected → summarize")
#         return "summarize"
    
#     if tool_calls:  # Agent wants more tools
#         return "tools"
#     return "summarize"  # Agent finished


