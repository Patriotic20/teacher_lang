import os
from dotenv import load_dotenv
from app.graph import build_graph

# Load API keys from the .env file
load_dotenv()

def main():
    # 1. Ensure the required local directories exist
    os.makedirs("data/inputs", exist_ok=True)
    os.makedirs("data/outputs", exist_ok=True)
    
    # 2. Build the LangGraph application
    app = build_graph()
    
    # 3. Define the input data (Make sure you put a test image in data/inputs/)
    inputs = {
        "image_path": "data/inputs/test_handwriting.jpg", 
        "rubric": "The student must correctly explain the process of photosynthesis, mentioning sunlight, water, and carbon dioxide. Total out of 10 points."
    }
    
    print("Starting the grading pipeline...")
    
    # 4. Run the workflow
    try:
        result = app.invoke(inputs)
        
        print("\n=== PIPELINE COMPLETE ===")
        print(f"Extracted Text:\n{result.get('extracted_text')}\n")
        print(f"Document Saved At: {result.get('doc_path')}\n")
        print(f"Teacher Feedback & Grade:\n{result.get('final_grade')}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()