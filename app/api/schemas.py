from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    service: str


class ProcessResponse(BaseModel):
    success: bool
    raw_text: str = ""
    entities: list[dict[str, Any]] = Field(default_factory=list)
    relationships: list[dict[str, Any]] = Field(default_factory=list)
    validation: list[dict[str, Any]] = Field(default_factory=list)
    fhir: dict[str, Any] | None = None
    error: str | None = None