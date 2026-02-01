def execute(client, concepts_data):
    """
    Generates a study roadmap based on extracted concepts.
    Args:
        concepts_data (str or dict): The output from the extract_concepts skill.
    Returns: JSON string with a 7-day study plan.
    """
    prompt = f"""
You are a JSON generator. Your ONLY task is to output valid JSON for a 7-day study roadmap based on the concepts below.

Concepts:
{concepts_data}

Rules:
1. Output ONLY valid JSON.
2. NO markdown, NO code blocks, NO text before or after.
3. Use double quotes for all keys and strings.
4. NO trailing commas.
5. Follow this EXACT structure:

{{
    "day1": {{"topic": "...", "activities": "...", "time_estimate": "..."}},
    "day2": {{"topic": "...", "activities": "...", "time_estimate": "..."}},
    "day3": {{"topic": "...", "activities": "...", "time_estimate": "..."}},
    "day4": {{"topic": "...", "activities": "...", "time_estimate": "..."}},
    "day5": {{"topic": "...", "activities": "...", "time_estimate": "..."}},
    "day6": {{"topic": "...", "activities": "...", "time_estimate": "..."}},
    "day7": {{"topic": "Review", "activities": "Review all topics", "time_estimate": "2 hours"}}
}}
"""
    response = client.generate_text(prompt)
    
    # Use the centralized JSON cleaner for consistency
    from utils.json_cleaner import clean_json_string
    return clean_json_string(response)
