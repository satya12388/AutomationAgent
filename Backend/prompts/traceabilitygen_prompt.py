traceability_template = '''
You are a QA Automation Expert.

Based on the following test cases and requirements, Generate a detailed traceability matrix in markdown format.
Traceability should include KPIs like how many TCs based on priority and like that, include test sign off criteria as well..Not pass count like that but quality gates that be checked before sign off.
Traceability should look enterprise grade and professional

requirement:
{requirement}

Test Cases:
{testcases}

Return only traceability matrix and no extra things, Heading Taceabilty matrix

'''