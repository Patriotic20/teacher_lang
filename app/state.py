from typing import TypedDict

class GradingState(TypedDict):
    image_path: str       
    extracted_text: str   
    doc_path: str         
    rubric: str           
    final_grade: str