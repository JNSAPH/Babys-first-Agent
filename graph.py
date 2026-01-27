from dotenv import load_dotenv


load_dotenv()

from core import logging  # noqa: F401 - Import to configure logging
import logging
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage

from core.state import State
from core.model import model
from core.nodes import prep_node, agent_node, tools_node, summarize_node
from core.nodes.token_node import token_node
from core.nodes.tools_node import route_agent



def build_graph():
    """Build and compile the agent workflow graph."""
    graph = StateGraph(State)

    # Add nodes
    graph.add_node("prep", prep_node)
    graph.add_node("agent", agent_node)
    graph.add_node("tokens", token_node)
    graph.add_node("tools", tools_node)
    graph.add_node("summarize", summarize_node)

    # Define workflow edges
    graph.add_edge(START, "prep")
    graph.add_edge("prep", "agent")
    graph.add_edge("agent", "tokens")  # Token counting after agent response
    graph.add_conditional_edges(
        "tokens",
        route_agent,
        {
            "tools": "tools",
            "summarize": "summarize",
        },
    )
    graph.add_edge("tools", "tokens")  # Loop: prep → agent → tokens → [tools? → tokens → agent → ...] → summarize → END
    graph.add_edge("summarize", END)

    return graph.compile()


if __name__ == "__main__":
    app = build_graph()
    
    result = app.invoke({
        "messages": [HumanMessage(content="Give me the weather for Tokyo. Also write a Haiku about Cherry Blossoms to a file named cherry.txt. After that in a seperate Request get the Weather for New York City.")],
        "research": "",
        "summary": ""
    })
    
    # print("\nFull Result:")
    # print(result)
    print("\nStructured Response:")
    print(result.get("structured_response", "No structured response."))

    print("\Tokens:")
    print(result.get("used_tokens", "No structured response."))

