import re
import json

def clean_json_string(text):
    """
    Cleans a string to extract valid JSON content.
    Handles Markdown code blocks, extra text, and LaTeX backslashes.
    """
    if not text:
        return ""
    
    # 1. Remove Markdown code blocks
    # This regex handles ```json ... ``` and normal ``` ... ```
    pattern = r"```(?:\w+)?\s*(.*?)\s*```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        text = match.group(1)
    
    # 2. Find the first '{'
    start_index = text.find('{')
    if start_index == -1:
        return text # No JSON object found
        
    # 3. Find the last '}'
    # If the JSON is truncated, the last '}' might be inside a string or nested object
    # resulting in invalid JSON.
    # We will try to parse from the largest possible substring down to the smallest
    # valid object.
    
    candidate = text[start_index:]
    
    # Try to clean LaTeX backslashes which are common causes of error
    # (e.g., \frac becomes invalid escape \f)
    # We replace single backslashes with double backslashes, ignoring valid JSON escapes.
    def escape_latex(s):
        # Negative lookbehind for backslash, match backslash, negative lookahead for valid escape chars
        return re.sub(r'(?<!\\)\\(?![\\/\"bfnrtu])', r'\\\\', s)

    # Attempt 1: Full substring from first { to last }
    end_index = candidate.rfind('}')
    if end_index != -1:
        attempt = candidate[:end_index+1]
        try:
            # Try parsing directly
            json.loads(attempt)
            return attempt
        except json.JSONDecodeError:
            try:
                # Try parsing with LaTeX fix
                fixed = escape_latex(attempt)
                json.loads(fixed)
                return fixed
            except json.JSONDecodeError:
                pass

    # Attempt 2: If model appended text after the JSON, the '}' we found might be correct,
    # but maybe we missed something. Or maybe the JSON is just malformed.
    # Let's try to find the balancing closing brace if possible.
    # Simple stack-based counter for { and }
    balance = 0
    scan_end_index = -1
    
    for i, char in enumerate(candidate):
        if char == '{':
            balance += 1
        elif char == '}':
            balance -= 1
            if balance == 0:
                scan_end_index = i
                break
    
    if scan_end_index != -1:
        exact_attempt = candidate[:scan_end_index+1]
        try:
            json.loads(exact_attempt)
            return exact_attempt
        except json.JSONDecodeError:
             # Try with LaTeX fix
            try:
                fixed = escape_latex(exact_attempt)
                json.loads(fixed)
                return fixed
            except json.JSONDecodeError:
                pass
                
    # If all else fails, return the best guess (first { to last })
    # and let the caller handle the error or show the raw string.
    if end_index != -1:
         return escape_latex(candidate[:end_index+1])
         
    return candidate
