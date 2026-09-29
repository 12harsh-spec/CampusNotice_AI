import json
from pathlib import Path
from .models import NoticeAnalysis

REQUIRED_FIELDS = [
    "notice_category",
    "title",
    "summary",
    "action_required",
    "deadline",
    "eligibility",
    "required_documents",
    "venue_or_submission_method",
    "fees",
    "contact_information",
    "important_points",
    "missing_information",
    "clarification_questions",
]

def structural_score(result: NoticeAnalysis) -> float:
    data = result.model_dump()
    passed = sum(field in data for field in REQUIRED_FIELDS)
    return passed / len(REQUIRED_FIELDS)

def load_cases():
    path = Path(__file__).resolve().parents[1] / "data" / "sample_notices.json"
    return json.loads(path.read_text(encoding="utf-8"))

if __name__ == "__main__":
    cases = load_cases()
    print(f"Evaluation cases: {len(cases)}")
    print(f"Required output fields: {len(REQUIRED_FIELDS)}")
    print("A valid Pydantic response provides 100% structural completeness.")
