def execute(client, text):
    """
    Creates a concise summary of the text.
    """
    prompt = f"""
You are a JSON generator. Summarize the text below into valid JSON.

Text:
{text}

Rules:
1. Output ONLY valid JSON.
2. NO markdown, NO code blocks.
3. NO trailing commas.
4. Follow this EXACT structure:

{{
  "title": "...",
  "summary": "...",
  "steps": [
    "Step 1",
    "Step 2",
    "Step 3"
  ]
}}
"""
    response = client.generate_text(prompt)
    
    # Use the centralized JSON cleaner for consistency
    from utils.json_cleaner import clean_json_string
    return clean_json_string(response)