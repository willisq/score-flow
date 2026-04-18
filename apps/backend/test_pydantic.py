from uuid import uuid4
from typing import List, Optional
from pydantic import BaseModel, Field

def to_camel(string: str) -> str:
    return string.split("_")[0] + "".join(word.capitalize() for word in string.split("_")[1:])

class TunedModel(BaseModel):
    class Config:
        populate_by_name = True
        alias_generator = to_camel

class PhysicalRequirementCreate(TunedModel):
    initial_weight: Optional[float] = Field(default=None, ge=0)
    final_weight: Optional[float] = Field(default=None, ge=0)

class CategoryModalityCreate(TunedModel):
    physical_requirements: List[PhysicalRequirementCreate] = []

payload = {
    "physicalRequirements": [
        {
            "initialWeight": 50,
            "finalWeight": 60
        }
    ]
}

obj = CategoryModalityCreate(**payload)
print("Parsed:", obj.model_dump())
