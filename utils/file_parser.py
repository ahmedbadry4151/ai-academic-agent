import io
from PyPDF2 import PdfReader

def parse_file(uploaded_file):
    """
    Extracts text from an uploaded file (PDF or TXT).
    Args:
        uploaded_file: A streamlit UploadedFile object.
    Returns:
        str: extracted text
    """
    if uploaded_file is None:
        return ""
    
    file_type = uploaded_file.name.split('.')[-1].lower()
    text = ""
    
    try:
        if file_type == 'pdf':
            pdf_reader = PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        elif file_type == 'txt':
            # read as bytes then decode
            text = uploaded_file.getvalue().decode("utf-8")
        else:
            return "Unsupported file type. Please upload PDF or TXT."
            
    except Exception as e:
        return f"Error reading file: {str(e)}"
        
    return text
