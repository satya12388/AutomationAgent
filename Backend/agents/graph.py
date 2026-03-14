from typing import TypedDict
from Backend.agents.nodes import f_extract_documents,f_extract_requirements,f_generate_testcases,f_review_testcases,f_export_csv,f_generate_scripts,f_traceabilty_matrix
from langgraph.graph import StateGraph,END
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()


class TestcasesState(TypedDict):
    file_path: str
    document_text: str
    requirements:object
    testcases: object
    review_status: str
    feedback:str
    csv_path:str
    script_path:str
    traceability_path:str

def review_decision(state):

    if state["review_status"] == "approved":
        return "approved"
    else:
        return "regenerate"
    

def build_graph():
    graph = StateGraph(TestcasesState)

    graph.add_node('n_extract_documents',f_extract_documents)
    graph.add_node('n_extract_requirements',f_extract_requirements)
    graph.add_node('n_generate_testcases',f_generate_testcases)
    graph.add_node('n_review_testcases',f_review_testcases)
    graph.add_node('n_export_csv',f_export_csv)
    graph.add_node('n_generate_scripts', f_generate_scripts)
    graph.add_node('n_traceability_matrix',f_traceabilty_matrix)

    graph.set_entry_point('n_extract_documents')
    graph.add_edge('n_extract_documents','n_extract_requirements')
    graph.add_edge('n_extract_requirements','n_generate_testcases')
    graph.add_edge('n_generate_testcases','n_review_testcases')

    graph.add_conditional_edges('n_review_testcases',
                                review_decision,
                                {
                                    "approved":'n_export_csv',
                                    "regenerate":'n_generate_testcases'
                                })
    graph.add_edge('n_export_csv','n_generate_scripts')
    graph.add_edge('n_generate_scripts','n_traceability_matrix')
    graph.add_edge('n_traceability_matrix',END)
    return graph.compile(checkpointer=memory)

agent = build_graph()



