"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any, Dict

from langgraph.graph import StateGraph
from langgraph.runtime import Runtime
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

from src.nodes import prep_node, agent_node, tools_node, output_node
from src.agent.state import State
from src.nodes.tools_node import route_agent
from src.nodes.token_node import token_node

logger = logging.getLogger(__name__)

def build_graph():
    """Build and compile the agent workflow graph."""
    logger.info("Building agent workflow graph")
    graph = StateGraph(State)

    # Add nodes
    graph.add_node("prep", prep_node)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tools_node)
    graph.add_node("output", output_node)
    logger.info("Added nodes: prep, agent, tools, output")

    # Define workflow edges
    graph.add_edge(START, "prep")
    graph.add_edge("prep", "agent")
    graph.add_conditional_edges(
        "agent",
        route_agent,
        {
            "tools": "tools",
            "output": "output",
        },
    )
    graph.add_edge("tools", "agent")  # Loop back to agent after tools
    graph.add_edge("output", END)
    logger.info("Workflow: START → prep → agent → [tools → agent]* → output → END")

    compiled = graph.compile()
    logger.info("Graph compiled successfully")
    return compiled

graph = build_graph()