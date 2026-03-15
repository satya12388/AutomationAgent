traceability_template = '''
Act as a senior Business Analyst and Software QA professional.

Create a professional Requirements Traceability Matrix (RTM) for the following project. The RTM must clearly map Business Requirements → Functional Requirements → Test Cases → Test Results → Responsible Owner.

Follow industry standards used in software development and quality assurance.

Include the following :
1. How many test cases were mapped to each requirement
2. How many test cases were mapped to priority
3. WHat are the test cases that has to be Passed before sign off
4. To Do Tasks for signing off the feature.


Formatting requirements:
- Present the RTM in a clean, professional format.
- Use clear requirement IDs like BR-01, FR-01, TC-01.
- Ensure traceability from requirement to testing.
- Make the matrix suitable for documentation in Excel or project reports.

Project Context:
[Insert your project description here]

Example:
Project: Online Food Delivery System
Modules: User Registration, Restaurant Search, Cart, Payment, Order Tracking

Also provide:
• A short explanation of how the RTM helps in project quality and requirement coverage.
• Best practices for maintaining the RTM during the project lifecycle.

requirement:
{requirement}

Test Cases:
{testcases}

Return only traceability matrix and no extra things, Heading Taceabilty matrix

'''