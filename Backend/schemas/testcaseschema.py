from pydantic import BaseModel, Field
from typing import List


class TestCase(BaseModel):
    requirement_id:str = Field(description='Which requirement that this test case will test')
    test_case_id: str
    title: str
    preconditions: str
    steps: List[str]
    expected_result: str
    priority: str


class TestCaseList(BaseModel):

    testcases: List[TestCase]