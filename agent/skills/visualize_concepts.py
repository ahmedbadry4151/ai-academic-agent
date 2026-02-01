import json
import os
try:
    import graphviz
except ImportError:
    graphviz = None

TOOL_SCHEMA = {
    "name": "generate_concept_map",
    "description": "Generates a visual concept map (PNG/SVG) from a list of concepts using Graphviz.",
    "input_schema": {
        "type": "object",
        "properties": {
            "concepts_data": {
                "type": "object",
                "description": "The JSON object containing extracted concepts, matching the output of extract_concepts."
            },
            "output_format": {
                "type": "string",
                "enum": ["png", "svg"],
                "default": "png"
            }
        },
        "required": ["concepts_data"]
    }
}

def execute(concepts_data, output_format="png"):
    """
    Generates a visual concept map from the provided concepts data.
    """
    if not graphviz:
        return "Error: Graphviz python library is not installed. Please install it."

    if isinstance(concepts_data, str):
        try:
            concepts_data = json.loads(concepts_data)
        except json.JSONDecodeError:
            return "Error: Invalid JSON string provided for visualization."

    # Create a new directed graph
    dot = graphviz.Digraph(comment='Concept Map', format=output_format)
    dot.attr(rankdir='LR')  # Left to right layout
    
    # Global node styles for a "comfortable" student look
    dot.attr('node', shape='box', style='filled', fillcolor='#E6F3FF', fontname='Arial', color='#4A90E2')
    dot.attr('edge', color='#999999')

    # Extract metadata
    metadata = concepts_data.get("document_metadata", {})
    main_topic = metadata.get("topic", "Main Topic")
    
    # Create the central node
    dot.node('ROOT', main_topic, shape='ellipse', fillcolor='#4A90E2', fontcolor='white', fontsize='14')

    extracted = concepts_data.get("extracted_concepts", [])
    
    for i, concept in enumerate(extracted):
        c_name = concept.get("concept_name", f"Concept {i+1}")
        c_def = concept.get("definition", "")
        
        # Create a clean label (name + truncated definition)
        short_def = (c_def[:50] + '...') if len(c_def) > 50 else c_def
        label = f"{c_name}\\n({short_def})"
        
        node_id = f"c_{i}"
        dot.node(node_id, label)
        
        # Connect to root
        dot.edge('ROOT', node_id)
        
        # Optional: Add formula or code nodes if present
        formula = concept.get("mathematical_formula")
        if formula and formula != "null":
            f_id = f"f_{i}"
            dot.node(f_id, f"Formula:\\n{formula}", shape='note', fillcolor='#FFF2CC', color='#D6B656')
            dot.edge(node_id, f_id, style='dashed')

    # Render the graph
    # We'll save it to a 'visualizations' folder
    output_dir = "visualizations"
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"concept_map_{main_topic.replace(' ', '_')}"
    output_path = os.path.join(output_dir, filename)
    
    try:
        # render() saves the file and returns the path
        # cleanup=True removes the source .dot file
        rendered_path = dot.render(output_path, view=False, cleanup=True)
        return f"Visualization generated successfully: {rendered_path}"
    except Exception as e:
        return f"Error generating visualization: {str(e)}. Ensure Graphviz is installed on your system PATH."
