import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from Backend.prompts.robotscriptgen_prompt import robotscript_template

model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

prompt = PromptTemplate(
    template = robotscript_template,
    input_variable = ['testcases']
)

def generate_robot_script(testcases):

    chain = prompt|model
    response = chain.invoke({'testcases':testcases})
    return response.content


def save_robot_script(script_text):

    os.makedirs("output", exist_ok=True)

    path = "output/generated_tests.robot"

    with open(path, "w", encoding="utf-8") as f:
        f.write(script_text)

    return path