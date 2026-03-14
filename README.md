# QA Automation Agent

An AI-powered application designed to streamline and automate Quality Assurance processes. The agent takes a raw Requirement Document (`.pdf`, `.doc`, `.docx`) as input and autonomously generates Test Cases, Robot Framework Automation Scripts, and a Traceability Matrix.

The system uses [Streamlit](https://streamlit.io/) for an interactive and professional frontend and leverages [LangGraph](https://python.langchain.com/docs/langgraph/) alongside large language models (via GroqCloud and OpenAI) for a robust semantic processing backend.

## Features

- **Document Extraction**: Upload `.pdf` or `.docx` formatted Requirement Documents.
- **Requirement Analysis**: Contextually parses text to understand system constraints and acceptance criteria.
- **Intelligent Test Case Generation**: Produces categorized test cases with Priority, Preconditions, detailed Steps, and Expected Results.
- **Human-in-the-Loop Review**: LangGraph interrupts the execution pipeline to present the generated test cases for Human Review. The user can Accept them or provide feedback to Regenerate.
- **Robot Framework Scripting**: AI automatically scaffolds ready-to-run automation testing scripts in Robot Framework syntax.
- **Traceability Matrix**: Generates a rich Markdown traceability matrix with KPIs and Quality Gate sign-off criteria linking Test Cases back to original Requirements.

## Technology Stack

- **Frontend**: Streamlit, Python
- **Backend**: LangChain, LangGraph, Pydantic (Structured Generation)
- **LLM Providers**: GroqCloud (`llama-3.1-8b-instant`, `openai/gpt-oss-120b`, `openai/gpt-oss-20b` via Groq)
- **Data Processing**: Pandas, pypdf, python-docx

## Project Structure

```text
QA Automation Agent/
├── Backend/
│   ├── agents/                   # LangGraph nodes and StateGraph construction (graph.py, nodes.py)
│   ├── prompts/                  # Prompt engineering templates for each distinct generation stage
│   ├── schemas/                  # Pydantic schemas for structured LLM JSON outputs
│   └── services/                 # Core logic services (document.py, testcasegenerator.py, etc.)
├── Frontend/
│   ├── app.py                    # Main Streamlit frontend UI
│   └── design/                   # Temporary directory for handling file uploads (auto-cleared)
├── Output/                       # Directory containing generated outputs (.csv, .robot, .md)
├── pyproject.toml                # UV Dependency configuration
├── requirements.txt              # Standard pip dependencies
└── README.md
```

## Setup & Installation

**Prerequisites**: Python 3.12+

1. **Clone the Repository**

   ```bash
   git clone <your-repo-url>
   cd QA-Automation-Agent
   ```

2. **Environment Setup**
   Create a `.env` file in the root directory and securely add your API Keys:

   ```env
   GROQ_API_KEY=gsk_your_api_key_here
   ```

3. **Install Dependencies**
   The project uses `uv` for lightning-fast dependency management, but supports standard pip as well.

   ```bash
   pip install -r requirements.txt
   ```

   _(Alternatively run `uv sync` if UV is installed)_

4. **Run the Application**
   Start the Streamlit development server:
   ```bash
   streamlit run Frontend/app.py
   ```

## Usage Workflow

1. Open the UI in your browser (`http://localhost:8501`).
2. Upload a requirement document (PDF or Word).
3. Click "Generate Test Cases" to begin the pipeline.
4. Review the generated Test Cases safely inside interactive `st.expander` modules.
5. Provide feedback or simply hit "Approve & Continue".
6. The app resumes the graph, generating the final Robot scripts and Traceability matrix.
7. Download all finalized artifacts securely from the Sidebar.
