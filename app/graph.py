from langgraph.graph import StateGraph, END
from app.state import GradingState
from app.nodes import extract_text_node, save_doc_node, grade_node

def build_graph():
    """Compiles the LangGraph workflow."""
    workflow = StateGraph(GradingState)
    
    # Add nodes
    workflow.add_node("extract", extract_text_node)
    workflow.add_node("save_doc", save_doc_node)
    workflow.add_node("grade", grade_node)
    
    # Define the execution flow
    workflow.set_entry_point("extract")
    workflow.add_edge("extract", "save_doc")
    workflow.add_edge("save_doc", "grade")
    workflow.add_edge("grade", END)
    
    return workflow.compile()