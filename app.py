import streamlit as st
from agent.orchestrator import Orchestrator
from utils.file_parser import parse_file
from utils.json_cleaner import clean_json_string
import os
import json

# Page config
st.set_page_config(page_title="AI Academic Agent", layout="wide")

def main():
    st.title("🎓 AI Academic Agent")
    st.markdown("### From Lecture Notes to Study Plan in Seconds")

    # Sidebar for setup
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("Watsonx API Key (Optional if set in .env)", type="password")
        project_id = st.text_input("Project ID (Optional if set in .env)", type="password")
        
        if api_key:
            os.environ["WATSONX_API_KEY"] = api_key
        if project_id:
            os.environ["WATSONX_PROJECT_ID"] = project_id

    # Initialize Orchestrator
    orchestrator = Orchestrator()

    # STEP 1: UPLOAD
    uploaded_file = st.file_uploader("Step 1: Upload your lecture notes (PDF/TXT)", type=["pdf", "txt"])

    if uploaded_file is not None:
        # STEP 2: PREPROCESSING
        with st.spinner("Reading file..."):
            text_content = parse_file(uploaded_file)
            st.success(f"File '{uploaded_file.name}' processed.")
            
            with st.expander("View extracted text"):
                st.text_area("Raw Text", text_content, height=150)

        st.divider()

        # STEP 3: AGENT INITIALIZATION & EXECUTION
        if st.button("🚀 Analyze & Generate Study Pack", type="primary"):
            
            progress_bar = st.progress(0)
            status_text = st.empty()

            try:
                # We can simulate progress updates or just run the batch
                status_text.text("Agent Initialized: Analyzing content...")
                progress_bar.progress(10)
                
                # The Orchestrator handles Steps 4, 5, and 6 internally
                results = orchestrator.handle_request("Generate Study Pack", text_content)
                
                progress_bar.progress(100)
                status_text.text("Analysis Complete!")
                
                # STEP 7: OUTPUT DELIVERY
                display_results(results)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

def display_results(results):
    """
    Renders the study pack components.
    """
    
    # 1. Key Concepts
    st.header("1. Key Concepts (Skill 1)")
    concepts_raw = results.get("concepts", "")
    
    if concepts_raw.startswith("Error"):
        st.error(concepts_raw)
    else:
        try:
            cleaned_concepts = clean_json_string(concepts_raw)
            concepts_data = json.loads(cleaned_concepts)
            
            # Helper to safely get data whether it's nested under "document_metadata" or flat
            # The schema defines "document_metadata" and "extracted_concepts"
            if "document_metadata" in concepts_data:
                difficulty = concepts_data["document_metadata"].get("difficulty_level", "Unknown")
            else:
                difficulty = concepts_data.get("difficulty", "Unknown")
                
            st.info(f"**Difficulty Level:** {difficulty}")
            
            # Handle different potential structures for list of concepts
            concepts_list = concepts_data.get("extracted_concepts", concepts_data.get("concepts", []))
            
            if concepts_list:
                for concept in concepts_list:
                    with st.container():
                        st.subheader(f"📌 {concept.get('concept_name', 'Concept')}")
                        
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"**Definition:**  \n{concept.get('definition', 'N/A')}")
                            st.markdown(f"**Problem Solved:**  \n{concept.get('problem_solved', 'N/A')}")
                        
                        with col2:
                            # Mathematical Formula
                            formula = concept.get("mathematical_formula")
                            if formula:
                                st.markdown("**Formula:**")
                                st.latex(formula)
                            
                            # Code Implementation
                            code = concept.get("code_implementation")
                            if code:
                                lib = code.get('library', 'Unknown Lib')
                                func = code.get('class_function', 'Unknown Func')
                                st.markdown(f"**Implementation:** `{lib}.{func}`")

                        # Limitations
                        limitations = concept.get("limitations")
                        if limitations:
                            st.markdown("**Limitations:**")
                            for lim in limitations:
                                st.markdown(f"- {lim}")
                        
                        st.divider()
            else:
                st.write("No specific concepts structured.")
                st.code(concepts_raw) # Fallback
        except json.JSONDecodeError:
            st.warning("Could not parse Concepts JSON. Raw output:")
            st.code(concepts_raw)

    st.divider()

    # 2. Study Roadmap
    st.header("2. 7-Day Study Roadmap (Skill 2)")
    roadmap_raw = results.get("roadmap", "")
    
    if roadmap_raw.startswith("Error"):
        st.error(roadmap_raw)
    else:
        try:
            cleaned_roadmap = clean_json_string(roadmap_raw)
            roadmap_data = json.loads(cleaned_roadmap)
            
            # Display as a timeline or formatted list
            for day, details in roadmap_data.items():
                with st.container():
                    # Handle if details is a string (rare but possible with some models) or dict
                    if isinstance(details, dict):
                        st.subheader(f"📅 {day.capitalize()}: {details.get('topic', 'Topic')}")
                        st.write(f"**Activities:** {details.get('activities', '')}")
                        st.caption(f"⏱️ Time Estimate: {details.get('time_estimate', '')}")
                    else:
                        st.subheader(f"📅 {day.capitalize()}")
                        st.write(str(details))
                        
        except json.JSONDecodeError:
            st.warning("Could not parse Roadmap JSON. Raw output:")
            st.code(roadmap_raw)

    st.divider()

    # 3. Summary
    st.header("3. Summary (Skill 3)")
    summary_raw = results.get("summary", "")
    
    if summary_raw.startswith("Error"):
         st.error(summary_raw)
    else:
        try:
            cleaned_summary = clean_json_string(summary_raw)
            summary_data = json.loads(cleaned_summary)
            
            st.subheader(summary_data.get("title", "Summary"))
            st.write(summary_data.get("summary", ""))
            
            steps = summary_data.get("steps", [])
            if steps:
                st.write("**Key Steps:**")
                for step in steps:
                    st.write(f"- {step}")
            
            # Prepare text for download
            download_text = f"# {summary_data.get('title', 'Summary')}\n\n"
            download_text += f"{summary_data.get('summary', '')}\n\n"
            if steps:
                download_text += "## Steps\n" + "\n".join([f"- {s}" for s in steps])
                
        except json.JSONDecodeError:
            st.warning("Could not parse Summary JSON. Raw output:")
            st.markdown(summary_raw)
            download_text = summary_raw

    # Download Button
    st.download_button(
        label="📥 Download Summary (.md)",
        data=download_text,
        file_name="study_summary.md",
        mime="text/markdown"
    )

    st.divider()

    # 4. Visual Summary
    st.header("4. Visual Concept Map (Skill 4)")
    visualization_raw = results.get("visualization", "")
    
    if "successfully" in visualization_raw:
        # Extract path from message: "Visualization generated successfully: path/to/file.png"
        image_path = visualization_raw.split(": ")[1].strip()
        if os.path.exists(image_path):
            st.image(image_path, caption="Concept Map", use_container_width=True)
            
            with open(image_path, "rb") as file:
                btn = st.download_button(
                        label="📥 Download Concept Map",
                        data=file,
                        file_name="concept_map.png",
                        mime="image/png"
                    )
        else:
             st.error(f"Image file not found at: {image_path}")
    else:
        st.warning(visualization_raw)

if __name__ == "__main__":
    main()