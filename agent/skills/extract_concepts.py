def execute(client, text):
    """
    Extracts key concepts from the text.
    Returns: JSON string with keys 'concepts' (list) and 'difficulty' (string).
    """
    # Using double braces for the JSON schema so Python f-string doesn't crash
    prompt = f"""
You are a JSON generator. Extract concepts from the text below into valid JSON.

Text:
{text}

Rules:
1. Output ONLY valid JSON.
2. NO markdown, NO code blocks.
3. NO trailing commas.
4. Follow this EXACT structure:

{{
  "document_metadata": {{
    "topic": "...",
    "difficulty_level": "Beginner"
  }},
  "extracted_concepts": [
    {{
      "concept_name": "...",
      "definition": "...",
      "problem_solved": "...",
      "mathematical_formula": "LaTeX or null",
      "code_implementation": {{
        "library": "...",
        "class_function": "..."
      }},
      "limitations": ["..."]
    }}
  ]
}}
"""

    response = client.generate_text(prompt)
    
    # Use the centralized JSON cleaner for consistency
    from utils.json_cleaner import clean_json_string
    return clean_json_string(response)