from langchain_groq import ChatGroq
from Backend.schemas.requirementschema import RequirementList
from langchain_core.prompts import PromptTemplate
from Backend.prompts.requirementgen_prompt import requirementgen_template


model = ChatGroq(model="llama-3.3-70b-versatile")
structured_model = model.with_structured_output(RequirementList)

prompt = PromptTemplate(
    template = requirementgen_template,
    input_variable = ['documents']
)


def extract_requirements(documents):

    chain = prompt | structured_model

    result = chain.invoke({"documents": documents})

    return result