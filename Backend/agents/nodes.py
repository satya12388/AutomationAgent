from Backend.services.documentloader import load_document
from Backend.services.testcasegenerator import generate_testcases
from Backend.services.csvexpoerter import export_to_csv 
from Backend.services.robotscriptgenerator import generate_robot_script,save_robot_script
from Backend.services.requirementgenerator import extract_requirements
from Backend.services.traceabilitygenerator import save_traceability,generate_traceability
from langgraph.types import interrupt



def f_extract_documents(state):
    print("\nExtracting Documents...\n")
    text = load_document(state["file_path"])

    return  {"document_text":text}

def f_extract_requirements(state):
    print("\nExtracting Requirements...\n")
    reqs = extract_requirements(state["document_text"])

    return {"requirements": reqs}

def f_generate_testcases(state):
    print("\nGenerating Testcases...\n")
    feedback = state.get('feedback',"")
    testcases = generate_testcases(state['requirements'],feedback)

    return  {"testcases":testcases}

def f_review_testcases(state):
    print("\nWaiting for human review...\n")

    return interrupt(
        {
            "testcases": state["testcases"]
        }
    )

def f_export_csv(state):
    print("\nExporting to CSV...\n")
    path = export_to_csv(state["testcases"])

    print(f"CSV saved to {path}")

    return {"csv_path": path}

def f_generate_scripts(state):

    print("\nGenerating automation scripts...\n")

    script = generate_robot_script(state["testcases"].model_dump())

    path = save_robot_script(script)

    print(f"\nRobot script saved at: {path}")

    return {"script_path": path}

def f_traceabilty_matrix(state):

    print("\nGenerating Traceability Matrix...\n")

    traceability_matrix = generate_traceability(state['requirements'].model_dump(),state["testcases"].model_dump())

    path = save_traceability(traceability_matrix)

    print(f"\nTraceability Matrix saved at: {path}")

    return {"traceability_path": path}