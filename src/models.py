from typing import Literal
from pydantic import BaseModel, Field

Category = Literal[
    "Exam",
    "Internship",
    "Placement",
    "Scholarship",
    "Event",
    "Administrative",
    "Fee",
    "Admission",
    "Other",
]

class NoticeAnalysis(BaseModel):
    notice_category: Category
    title: str
    summary: str
    action_required: list[str] = Field(default_factory=list)
    deadline: str | None = None
    eligibility: list[str] = Field(default_factory=list)
    required_documents: list[str] = Field(default_factory=list)
    venue_or_submission_method: str | None = None
    fees: str | None = None
    contact_information: list[str] = Field(default_factory=list)
    important_points: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    clarification_questions: list[str] = Field(default_factory=list)
