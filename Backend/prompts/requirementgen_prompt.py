requirementgen_template = """
You are a QA analyst.

Extract clear functional requirements from the following document.

Rules:
- Assign unique IDs like REQ-001, REQ-002
- Only functional requirements
- Keep descriptions concise

Max 5 requirements
Return the output STRICTLY matching the schema.

Do not include explanations.
Do not include markdown.
Return valid JSON only.

Document:
{documents}
"""