from langgraph.graph import StateGraph, START, END
from agent.state import AgentState
from agent.nodes import design_grna, scan_genome, score_sites, make_verdict

# creating the graph
graph = StateGraph(AgentState)

# adding nodes
graph.add_node("design_grna", design_grna)
graph.add_node("scan_genome", scan_genome)
graph.add_node("score_sites", score_sites)
graph.add_node("make_verdict", make_verdict)

# adding edges
graph.add_edge(START, "design_grna")
graph.add_edge("design_grna", "scan_genome")
graph.add_edge("scan_genome", "score_sites")
graph.add_edge("score_sites", "make_verdict")
graph.add_edge("make_verdict", END)

#Compile
app = graph.compile()
