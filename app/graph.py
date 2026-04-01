"""
graph.py – LangGraph workflow definition

Flow:
  load_teacher_answers → extract_text → save_doc → grade → END
"""

from langgraph.graph import StateGraph, END

from app.nodes import (
    load_teacher_answers_node,
    extract_text_node,
    save_doc_node,
    grade_node,
)
from app.state import GradingState


def build_graph():
    """Compile and return the grading workflow."""
    workflow = StateGraph(GradingState)

    # Register nodes
    workflow.add_node("load_teacher_answers", load_teacher_answers_node)
    workflow.add_node("extract_text",         extract_text_node)
    workflow.add_node("save_doc",             save_doc_node)
    workflow.add_node("grade",                grade_node)

    # Define linear pipeline
    workflow.set_entry_point("load_teacher_answers")
    workflow.add_edge("load_teacher_answers", "extract_text")
    workflow.add_edge("extract_text",         "save_doc")
    workflow.add_edge("save_doc",             "grade")
    workflow.add_edge("grade",                END)

    return workflow.compile()