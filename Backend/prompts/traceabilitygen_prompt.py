traceability_template = '''
Act as a senior Business Analyst and Software QA professional.

Create a professional Requirements Traceability Matrix (RTM) for the following project. The RTM must clearly map Business Requirements → Functional Requirements → Test Cases → Test Results → Responsible Owner.

Follow industry standards used in software development and quality assurance.

Include the following columns in the table:
1. Requirement ID
2. Business Requirement Description
3. Functional Requirement
4. Module / Feature
5. Priority (High/Medium/Low)
6. Test Case ID
7. Test Case Description
Below should be blank and ask tester to update
8. Test Status (Pass/Fail/Blocked)
9. Responsible Team/Owner
10. Comments

Formatting requirements:
- Present the RTM in a clean, professional table format.
- Use clear requirement IDs like BR-01, FR-01, TC-01.
- Ensure traceability from requirement to testing.
- Add at least 8–10 example entries.
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