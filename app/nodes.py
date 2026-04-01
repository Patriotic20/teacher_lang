import base64
from docx import Document
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from app.state import GradingState

def extract_text_node(state: GradingState):
    """Uses a Vision LLM to read the handwritten image."""
    # Open and encode the image
    with open(state["image_path"], "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Initialize the Vision model 
    vision_llm = ChatOpenAI(model="gpt-4o", max_tokens=1000)
    
    message = HumanMessage(
        content=[
            {"type": "text", "text": "Extract all handwritten text from this image exactly as written. Do not add any extra commentary or markdown formatting."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_string}"}}
        ]
    )
    
    response = vision_llm.invoke([message])
    return {"extracted_text": response.content}


def save_doc_node(state: GradingState):
    """Saves the extracted text to a .docx file."""
    doc = Document()
    doc.add_heading('Student Answer Transcription', 0)
    doc.add_paragraph(state["extracted_text"])
    
    # Save to the outputs directory
    doc_path = "data/outputs/student_answer.docx"
    doc.save(doc_path)
    
    return {"doc_path": doc_path}


def grade_node(state: GradingState):
    """Uses a Smart LLM to grade the extracted text against a rubric."""
    smart_llm = ChatOpenAI(model="gpt-4o", temperature=0.1) # Low temp for consistent grading
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert teacher grading a student's answer based on a strict rubric. Be fair, point out specific mistakes, and assign a final score."),
        ("user", "Rubric:\n{rubric}\n\nStudent Answer:\n{answer}\n\nPlease provide a grade and feedback.")
    ])
    
    chain = prompt | smart_llm
    response = chain.invoke({
        "rubric": state["rubric"], 
        "answer": state["extracted_text"]
    })
    
    return {"final_grade": response.content}