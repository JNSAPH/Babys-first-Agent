from src.agent.graph import graph

graph_mermaid_png  = graph.get_graph().draw_mermaid_png()
with open("graph_export.png", "wb") as f:
    f.write(graph_mermaid_png)