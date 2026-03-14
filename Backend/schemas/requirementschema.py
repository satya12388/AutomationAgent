from pydantic import BaseModel
from typing import List

class Requirement(BaseModel):
    requirement_id: str
    description: str


class RequirementList(BaseModel):
    requirements: List[Requirement]