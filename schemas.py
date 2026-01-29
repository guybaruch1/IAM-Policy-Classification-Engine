"""Output schema and validation for policy classification results."""
from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field, validator


class ClassificationOutput(BaseModel):
	classification: Literal["Weak", "Strong"] = Field(..., description="Policy classification label")
	reason: str = Field(..., min_length=5, max_length=1000, description="Concise security-focused explanation")

	@validator("reason")
	def reason_must_be_concise(cls, v: str) -> str:
		# Encourage short, focused reasons
		if len(v.split()) > 120:
			raise ValueError("reason is too long; keep it concise")
		return v.strip()


__all__ = ["ClassificationOutput"]