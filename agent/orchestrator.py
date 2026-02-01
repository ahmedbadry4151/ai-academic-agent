from utils.watsonx_client import WatsonxClient
from agent.skills import extract_concepts, generate_roadmap, create_summary, visualize_concepts, search_pdfs

class Orchestrator:
    def __init__(self):
        self.client = WatsonxClient()

    def generate_study_pack(self, text):
        """
        Executes the full 7-step workflow:
        1. Extract Concepts (Step 4)
        2. Generate Roadmap using Concepts (Step 5)
        3. Create Summary (Step 6)
        """
        # Step 4: Concept Extraction
        concepts_json = extract_concepts.execute(self.client, text)
        
        # Step 5: Roadmap Generation (Uses the output of Step 4)
        # We pass the raw JSON string of concepts to the roadmap generator
        roadmap_json = generate_roadmap.execute(self.client, concepts_json)
        
        # Step 6: Summary Generation
        summary_text = create_summary.execute(self.client, text)

        # Step 7: Visualization
        visualization_result = visualize_concepts.execute(concepts_json)
        
        return {
            "concepts": concepts_json,
            "roadmap": roadmap_json,
            "summary": summary_text,
            "visualization": visualization_result
        }

    def handle_request(self, task_type, text):
        """
        Routes the request to the appropriate skill.
        """
        if not text:
            return "Please provide text content to process."

        if task_type == "Generate Study Pack":
             return self.generate_study_pack(text)
        elif task_type == "Extract Concepts":
            return extract_concepts.execute(self.client, text)
        elif task_type == "Generate Roadmap":
            # Note: This fallback might be less accurate without the concept step, 
            # but we'll keep it for direct access if needed.
            return generate_roadmap.execute(self.client, text)
        elif task_type == "Create Summary":
            return create_summary.execute(self.client, text)
        elif task_type == "Visual Summary":
            # Chain: Extract Concepts -> Visualize
            # First, we need the structured concepts
            concepts_json = extract_concepts.execute(self.client, text)
            # Then we pass that JSON to the visualizer
            return visualize_concepts.execute(concepts_json)
        elif task_type == "Search PDFs":
            # Treat 'text' as the search query
            return search_pdfs.execute(query=text)
        else:
            return "Unknown task type."
