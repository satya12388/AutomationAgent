from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from Backend.prompts.testcasegen_prompt import testcase_template
from Backend.schemas.testcaseschema import TestCaseList
load_dotenv()

## Function to return Test Cases from AI

model = ChatGroq(model="llama-3.3-70b-versatile")
structured_model = model.with_structured_output(TestCaseList)

prompt = PromptTemplate(
    template = testcase_template,
    input_variable = ['requirement','feedback']
)

def generate_testcases(requirement,feedback = ""):

    chain = prompt|structured_model
    result = chain.invoke({
        'requirement':requirement,
        'feedback':feedback
    })

    return result
