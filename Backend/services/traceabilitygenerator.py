import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from Backend.prompts.traceabilitygen_prompt import traceability_template

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

prompt = PromptTemplate(
    template = traceability_template,
    input_variable = ['requirement','testcases']
)

def generate_traceability(requirement,testcases):

    chain = prompt|model
    response = chain.invoke({
        'requirement':requirement,
        'testcases':testcases})
    return response.content


def save_traceability(traceability_matrix):

    os.makedirs("output", exist_ok=True)

    path = "output/traceability_matrix.md"

    with open(path, "w", encoding="utf-8") as f:
        f.write(traceability_matrix)

    return path