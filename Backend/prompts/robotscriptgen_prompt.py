robotscript_template = """
You are a QA Automation Engineer.

Convert the following test cases into a Robot Framework Selenium automation script.if you dnot know Xpaths, or ID keep it as variables section and add comment to update by the user.

Requirements:
- Use Robot Framework syntax
- Use SeleniumLibrary
- Each test case should become a Robot test case
- Use clear keywords
- Include Setup and Teardown
- Use good naming conventions
- if any keywords make sure you have keywords section and define all the keywords in the keywords section.
- make sure the script is without any errors and is of production quality.
- Dont give blank file.

Return ONLY the Robot Framework script directly no explainations nothing extra including nheadings or comments only robot script.

Test Cases:
{testcases}
"""