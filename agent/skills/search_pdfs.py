import os
import json

TOOL_SCHEMA = {
    "name": "search_study_pdfs",
    "description": "Searches for PDF files in the study directory and subdirectories.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Optional keyword to filter filenames. If empty, lists all PDFs."
            },
            "root_directory": {
                "type": "string",
                "description": "The root directory to search. Defaults to current directory."
            }
        }
    }
}

def execute(query=None, root_directory="."):
    """
    Searches for PDF files in the specified directory recursively.
    """
    pdf_files = []
    
    # Walk through the directory
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.lower().endswith(".pdf"):
                # If a query is provided, check if it matches the filename
                if query and query.lower() not in file.lower():
                    continue
                
                full_path = os.path.join(root, file)
                pdf_files.append({
                    "filename": file,
                    "path": full_path,
                    "directory": root
                })
    
    if not pdf_files:
        return json.dumps({"status": "no_results", "message": "No PDFs found."})
        
    return json.dumps({
        "status": "success",
        "count": len(pdf_files),
        "files": pdf_files
    }, indent=2)
