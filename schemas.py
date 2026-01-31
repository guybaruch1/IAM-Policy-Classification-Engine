"""Output schema and validation for policy classification results."""

from typing import Literal
from pydantic import BaseModel, Field


class ClassificationOutput(BaseModel):
    classification: Literal["Weak", "Strong"] = Field(
        ..., description="Policy classification label"
    )
    reason: str = Field(
        ..., min_length=5, max_length=1000,
        description="Concise security-focused explanation"
    )

    model_config = {
        "extra": "forbid"
    }
