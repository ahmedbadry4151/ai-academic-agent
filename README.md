# AI Academic Agent

An AI-powered assistant to help students process academic materials. It can summarize texts, extract key concepts, and generate study roadmaps using IBM Watsonx.ai.

## Features

- **File Support**: Upload PDF or TXT files.
- **Summarization**: Get concise summaries of long documents.
- **Concept Extraction**: Identify key terms and definitions.
- **Study Roadmap**: Generate a step-by-step learning plan based on the content.

## Setup

1.  **Clone the repository** (or ensure you are in the project folder).

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Variables**:
    Create a `.env` file in the root directory (`ai-academic-agent/.env`) with your IBM Watsonx credentials:
    ```env
    WATSONX_API_KEY=your_api_key_here
    WATSONX_PROJECT_ID=your_project_id_here
    WATSONX_URL=https://us-south.ml.cloud.ibm.com
    ```
    *Alternatively, you can enter these directly in the Streamlit sidebar.*

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

## Project Structure

- `app.py`: The frontend application (Streamlit).
- `agent/`: Contains the orchestrator and AI skills.
- `utils/`: Helper functions for file parsing and API communication.
