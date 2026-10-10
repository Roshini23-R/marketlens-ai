from app.agents.state import ResearchState
from app.agents.nodes.planner import planner_node
# from app.agents.nodes.mock_search import mock_search
from app.agents.nodes.report_writter import report_writer_node
from app.agents.nodes.web_search import web_search_node
from app.agents.nodes.report_synthesizer import report_synthesizer_node
from langgraph.graph import StateGraph,START,END 


def build_research_graph():
    graph = StateGraph(ResearchState)
    graph.add_node( "planner",planner_node)
    graph.add_node( "web-search",web_search_node)
    
    graph.add_node("report_synthesizer", report_synthesizer_node)

    graph.add_edge(START,"planner")
    graph.add_edge("planner", "web-search")
    graph.add_edge("web-search", "report_synthesizer")
    graph.add_edge("report_synthesizer", END)
    compiled_graph = graph.compile()
    return compiled_graph
research_graph=build_research_graph()