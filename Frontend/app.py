import streamlit as st
import os
import shutil
import uuid
import sys

# Ensure the parent directory is in the path to import Backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Backend.agents.graph import agent
from langgraph.types import Command

st.set_page_config(page_title="QA Automation Agent", page_icon="🤖", layout="wide")

def rerun_app():
    if hasattr(st, 'rerun'):
        st.rerun()
    elif hasattr(st, 'experimental_rerun'):
        st.experimental_rerun()
    else:
        st._rerun()

DESIGN_DIR = os.path.join(os.path.dirname(__file__), "design")

def clear_design_folder():
    if os.path.exists(DESIGN_DIR):
        shutil.rmtree(DESIGN_DIR)
    os.makedirs(DESIGN_DIR, exist_ok=True)

# Initialize Session State
if "initialized" not in st.session_state:
    clear_design_folder()
    st.session_state.initialized = True
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.file_path = None
    st.session_state.graph_stage = "upload" # upload -> running -> review -> running_final -> completed
    st.session_state.testcases = None
    st.session_state.results = {}

def reset_session():
    clear_design_folder()
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.file_path = None
    st.session_state.graph_stage = "upload"
    st.session_state.testcases = None
    st.session_state.results = {}
    rerun_app()

st.title("🤖 QA Automation Agent")
st.markdown("Upload a requirement document (PDF or Word) to generate Test Cases, Robot Framework Scripts, and a Traceability Matrix.")

with st.sidebar:
    st.header("Settings")
    if st.button("Reset Session", type="primary"):
        reset_session()
    
    st.markdown("---")
    st.markdown("### Process Status")
    if st.session_state.graph_stage == "upload":
        st.info("Waiting for file upload...")
    elif st.session_state.graph_stage == "running":
        st.warning("Generating Test Cases...")
    elif st.session_state.graph_stage == "review":
        st.error("Waiting for Human Review!")
    elif st.session_state.graph_stage == "running_final":
        st.warning("Generating Final Artifacts...")
    elif st.session_state.graph_stage == "completed":
        st.success("Completed!")

# Helper to run the graph and show progress
def run_agent_stream(inputs, config, status_container, progress_bar, is_resume=False):
    status_text = status_container.empty()
    node_mapping = {
        "n_extract_documents": "Extracting Document Content...",
        "n_extract_requirements": "Analyzing Requirements...",
        "n_generate_testcases": "Generating Test Cases...",
        "n_review_testcases": "Human Review Stage...",
        "n_export_csv": "Exporting Test Cases to CSV...",
        "n_generate_scripts": "Generating Robot Framework Script...",
        "n_traceability_matrix": "Generating Traceability Matrix..."
    }
    
    total_steps = len(node_mapping)
    current_step = 0
    
    try:
        # stream the agent
        for event in agent.stream(inputs, config=config, stream_mode="updates"):
            for node_name, node_state in event.items():
                current_step += 1
                progress = min(current_step / total_steps, 1.0)
                if progress_bar is not None:
                    progress_bar.progress(progress)
                
                friendly_name = node_mapping.get(node_name, f"Running {node_name}...")
                status_text.info(friendly_name)
    except Exception as e:
        status_text.error(f"Error during execution: {str(e)}")
        return

    # Check state after stream
    state = agent.get_state(config)
    
    # Check if there are tasks running or interrupted
    if len(state.tasks) > 0:
        task = state.tasks[0]
        if task.interrupts:
            st.session_state.graph_stage = "review"
            st.session_state.testcases = state.values.get("testcases")
            rerun_app()
            return
            
    if not state.next:
        st.session_state.graph_stage = "completed"
        st.session_state.results = {
            "csv_path": state.values.get("csv_path"),
            "script_path": state.values.get("script_path"),
            "traceability_path": state.values.get("traceability_path")
        }
        rerun_app()

config = {"configurable": {"thread_id": st.session_state.thread_id}}

if st.session_state.graph_stage == "upload":
    st.markdown("### 1. Upload Requirements")
    uploaded_file = st.file_uploader("Upload Requirement Document", type=["pdf", "doc", "docx"])
    
    if uploaded_file is not None:
        file_path = os.path.join(DESIGN_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.session_state.file_path = file_path
        st.success(f"File uploaded successfully: {uploaded_file.name}")
        
        if st.button("Generate Test Cases", type="primary", use_container_width=True):
            st.session_state.graph_stage = "running"
            rerun_app()

elif st.session_state.graph_stage == "running":
    st.subheader("Processing Document...")
    progress_bar = st.progress(0)
    status_container = st.container()
    
    inputs = st.session_state.get("resume_command", None)
    if inputs:
        st.session_state.resume_command = None # Clear it
        run_agent_stream(inputs, config, status_container, progress_bar)
    else:
        inputs = {"file_path": st.session_state.file_path}
        run_agent_stream(inputs, config, status_container, progress_bar)

elif st.session_state.graph_stage == "review":
    st.subheader("📝 Review Generated Test Cases")
    
    testcases = st.session_state.testcases
    if testcases:
        # Check if it's the Pydantic object
        if hasattr(testcases, "model_dump"):
            tc_data = testcases.model_dump().get("testcases", [])
        elif isinstance(testcases, dict) and "testcases" in testcases:
            tc_data = testcases["testcases"]
        else:
            tc_data = []

        if tc_data:
            for i, tc in enumerate(tc_data):
                with st.expander(f"{tc.get('test_case_id', f'TC-{i+1}')}: {tc.get('title', 'Untitled')}"):
                    st.markdown(f"**Requirement ID:** {tc.get('requirement_id', 'N/A')}")
                    st.markdown(f"**Priority:** {tc.get('priority', 'N/A')}")
                    st.markdown(f"**Preconditions:** {tc.get('preconditions', 'None')}")
                    
                    st.markdown("**Steps:**")
                    steps = tc.get("steps", [])
                    for idx, step in enumerate(steps):
                        st.markdown(f"{idx + 1}. {step}")
                        
                    st.markdown(f"**Expected Result:** {tc.get('expected_result', 'N/A')}")
        else:
            if hasattr(testcases, "model_dump"):
                st.json(testcases.model_dump())
            else:
                st.write(testcases)
    
    st.markdown("---")
    st.subheader("Provide Feedback")
    feedback = st.text_area("Feedback (optional, used if rejected)", placeholder="e.g. Include more negative test cases for user login.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Approve & Continue", type="primary", use_container_width=True):
            st.session_state.graph_stage = "running_final"
            st.session_state.resume_command = Command(resume={"review_status": "approved", "feedback": feedback})
            rerun_app()
            
    with col2:
        if st.button("❌ Reject & Regenerate", type="secondary", use_container_width=True):
            st.session_state.graph_stage = "running"
            st.session_state.resume_command = Command(resume={"review_status": "regenerate", "feedback": feedback})
            rerun_app()

elif st.session_state.graph_stage == "running_final":
    st.subheader("Completing Execution...")
    progress_bar = st.progress(0.5)
    status_container = st.container()
    
    # Retrieve the saved resume command 
    inputs = st.session_state.get("resume_command", None)
    if inputs:
        st.session_state.resume_command = None # Clear it
        run_agent_stream(inputs, config, status_container, progress_bar, is_resume=True)
    else:
        st.error("No resume command found. Something went wrong.")

elif st.session_state.graph_stage == "completed":
    st.subheader("Generation Complete")
    st.success("All artifacts have been successfully generated. You can download them from the sidebar.")

    results = st.session_state.results
    
    # 1. Main screen previews
    st.markdown("### Preview Artifact")
    
    preview_selection = st.radio(
        "Select file to preview:",
        ["Test Cases (CSV)", "Robot Script", "Traceability Matrix"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if preview_selection == "Test Cases (CSV)":
        csv_path = results.get("csv_path")
        if csv_path and os.path.exists(csv_path):
            try:
                with open(csv_path, "r", encoding='utf-8') as f:
                    csv_text = f.read()
                
                # Render the CSV as raw text in a nice code block so it always works
                # and bypasses all Pandas/PyArrow errors completely.
                st.code(csv_text, language="csv")
            except Exception as e:
                st.error(f"Error reading CSV file: {str(e)}")
        else:
            st.error(f"CSV file not found.")
            
    elif preview_selection == "Robot Script":
        script_path = results.get("script_path")
        if script_path and os.path.exists(script_path):
            with open(script_path, "r", encoding='utf-8') as f:
                script_content = f.read()
            st.code(script_content, language="robotframework")
        else:
            st.error(f"Robot script file not found.")
            
    elif preview_selection == "Traceability Matrix":
        trace_path = results.get("traceability_path")
        if trace_path and os.path.exists(trace_path):
            with open(trace_path, "r", encoding='utf-8') as f:
                trace_content = f.read()
            st.markdown(trace_content)
        else:
            st.error(f"Traceability Matrix not found.")

    st.markdown("---")
    if st.button("Start New Session", type="primary"):
        reset_session()

# Sidebar display logic for completed artifacts
if st.session_state.graph_stage == "completed":
    with st.sidebar:
        st.markdown("---")
        st.markdown("### Download Artifacts")
        
        results = st.session_state.results
        
        # Test Cases CSV
        csv_path = results.get("csv_path")
        if csv_path and os.path.exists(csv_path):
            with open(csv_path, "rb") as f:
                csv_bytes = f.read()
            st.download_button("📥 Download Test Cases (CSV)", csv_bytes, file_name=os.path.basename(csv_path), mime="text/csv", use_container_width=True)
                    
        # Robot Script
        script_path = results.get("script_path")
        if script_path and os.path.exists(script_path):
            with open(script_path, "r", encoding='utf-8') as f:
                script_content = f.read()
            st.download_button("📥 Download Robot Script", script_content, file_name=os.path.basename(script_path), mime="text/plain", use_container_width=True)
                
        # Traceability Matrix
        trace_path = results.get("traceability_path")
        if trace_path and os.path.exists(trace_path):
            with open(trace_path, "r", encoding='utf-8') as f:
                trace_content = f.read()
            st.download_button("📥 Download Matrix", trace_content, file_name=os.path.basename(trace_path), mime="text/plain", use_container_width=True)
