from dotenv import load_dotenv

load_dotenv()

from core import logging  # noqa: F401 - Import to configure logging
import logging
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage

from core.state import State
from core.model import model
from core.nodes import prep_node, agent_node, tools_node, summarize_node
from core.nodes.tools_node import route_agent



def build_graph():
    """Build and compile the agent workflow graph."""
    graph = StateGraph(State)

    # Add nodes
    graph.add_node("prep", prep_node)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tools_node)
    graph.add_node("summarize", summarize_node)

    # Define workflow edges
    graph.add_edge(START, "prep")
    graph.add_edge("prep", "agent")
    graph.add_conditional_edges(
        "agent",
        route_agent,
        {
            "tools": "tools",
            "summarize": "summarize",
        },
    )
    graph.add_edge("tools", "agent")  # Loop: agent → tools → agent
    graph.add_edge("summarize", END)

    return graph.compile()


if __name__ == "__main__":
    app = build_graph()
    
    result = app.invoke({
        "messages": [HumanMessage(content="Get the weather for Cuxhaven and write it to /tmp/weather.txt")],
        "research": "",
        "summary": ""
    })
    
    print(result["summary"])


