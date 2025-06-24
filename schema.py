from pydantic import BaseModel, Field
from typing import List

class RiskLevelOutput(BaseModel):
    risk_level: str = Field(
        description="The assessed risk level based on the patient's reported symptoms. Should be one of: Low, Medium, High."
    )
    explanation: str = Field(
        description="A clear, empathetic explanation of why this risk level was chosen."
    )
    suggestions: List[str] = Field(
        description="A list of actionable suggestions or steps the patient should take."
    )
    additional_notes: str = Field(
        default="",
        description="extra insights, advice, or reassurance for the patient."
    )