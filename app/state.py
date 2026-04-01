from typing import TypedDict, Optional


class GradingState(TypedDict):
    # --- Inputs ---
    image_path: str           # Path to student's handwritten image
    teacher_doc_path: str     # Path to teacher's .docx answer file
    rubric: str               # Grading rubric (max points, criteria, etc.)

    # --- Intermediate ---
    extracted_text: str       # OCR result from Gemini
    teacher_answers: str      # Parsed text from teacher's .docx
    doc_path: str             # Path where student answer .docx is saved

    # --- Output ---
    final_grade: str          # Claude's grading feedback + score