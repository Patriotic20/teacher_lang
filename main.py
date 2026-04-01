"""
main.py – Entry point for the AI grading pipeline

Usage:
    python main.py

Required environment variables (.env):
    GEMINI_API_KEY      – Google AI Studio key  (for OCR)
    ANTHROPIC_API_KEY   – Anthropic key          (for grading)

Required files:
    data/inputs/student_image.jpg       – student's handwritten answer image
    data/inputs/teacher_answers.docx    – teacher's model answer document

Output:
    data/outputs/student_answer.docx    – transcribed student answer
    Console: grade + feedback from Claude
"""

import logging
import os
import sys

from dotenv import load_dotenv

from app.graph import build_graph

# ── Logging setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s – %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ── Validation ────────────────────────────────────────────────────────────────

def _check_env() -> None:
    """Abort early if required API keys are missing."""
    missing = [k for k in ("GEMINI_API_KEY", "ANTHROPIC_API_KEY") if not os.getenv(k)]
    if missing:
        logger.error("Missing environment variables: %s", ", ".join(missing))
        logger.error("Add them to your .env file and re-run.")
        sys.exit(1)


def _check_files(*paths: str) -> None:
    """Abort early if required input files are missing."""
    for p in paths:
        if not os.path.exists(p):
            logger.error("Required file not found: %s", p)
            sys.exit(1)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    load_dotenv()
    _check_env()

    # Ensure directory structure
    os.makedirs("data/inputs",  exist_ok=True)
    os.makedirs("data/outputs", exist_ok=True)

    # ── Configure your inputs here ──────────────────────────────────────────
    STUDENT_IMAGE    = "data/inputs/student_image.jpg"
    TEACHER_DOC      = "data/inputs/teacher_answers.docx"
    RUBRIC = (
        "This answer is worth 10 points total.\n"
        "Award points as follows:\n"
        "  - 3 pts: Correctly identifies the role of sunlight\n"
        "  - 3 pts: Mentions water (H₂O) as a reactant\n"
        "  - 3 pts: Mentions carbon dioxide (CO₂) as a reactant\n"
        "  - 1 pt:  States that glucose/oxygen are produced\n"
        "Deduct points for factual errors. Give 0 for blank or off-topic answers."
    )
    # ────────────────────────────────────────────────────────────────────────

    _check_files(STUDENT_IMAGE, TEACHER_DOC)

    inputs = {
        "image_path":       STUDENT_IMAGE,
        "teacher_doc_path": TEACHER_DOC,
        "rubric":           RUBRIC,
    }

    logger.info("Starting grading pipeline…")
    logger.info("  Student image  : %s", STUDENT_IMAGE)
    logger.info("  Teacher answers: %s", TEACHER_DOC)

    app = build_graph()

    try:
        result = app.invoke(inputs)
    except FileNotFoundError as e:
        logger.error("File error: %s", e)
        sys.exit(1)
    except ValueError as e:
        logger.error("Value error: %s", e)
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        sys.exit(1)

    # ── Print results ──────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  GRADING PIPELINE COMPLETE")
    print("=" * 60)
    print(f"\n📄 Extracted Student Text:\n{result.get('extracted_text')}\n")
    print(f"💾 Student Answer Doc saved at: {result.get('doc_path')}\n")
    print(f"📝 Teacher Feedback & Grade:\n{result.get('final_grade')}\n")
    print("=" * 60)


if __name__ == "__main__":
    main()