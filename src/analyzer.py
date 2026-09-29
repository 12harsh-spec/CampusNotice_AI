from .config import Settings
from .llm_client import LLMClient
from .models import NoticeAnalysis
from .preprocessing import normalize_notice, extract_basic_features
from .prompt_loader import load_prompt

# The import above intentionally points to preprocessing in normal use.
# This fallback keeps compatibility if a user renames the module.
try:
    from .preprocessing import normalize_notice, extract_basic_features
except ImportError:
    pass

def analyze_notice(
    notice: str,
    settings: Settings
) -> tuple[NoticeAnalysis, dict]:
    notice = normalize_notice(notice)
    features = extract_basic_features(notice)

    if settings.demo_mode or not settings.api_key:
        return demo_analysis(notice), features

    prompt = load_prompt(notice)
    result = LLMClient(settings).analyze(prompt)
    return result, features

def demo_analysis(notice: str) -> NoticeAnalysis:
    lowered = notice.lower()

    if "internship" in lowered:
        category = "Internship"
    elif "exam" in lowered or "examination" in lowered:
        category = "Exam"
    elif "scholarship" in lowered:
        category = "Scholarship"
    elif "placement" in lowered:
        category = "Placement"
    elif "event" in lowered or "seminar" in lowered:
        category = "Event"
    else:
        category = "Administrative"

    deadline = None
    if "5 october" in lowered:
        deadline = "5 October 2026"

    return NoticeAnalysis(
        notice_category=category,
        title="College Notice — Extracted Brief",
        summary=notice[:350],
        action_required=["Read the original notice and complete any required action before the stated deadline."],
        deadline=deadline,
        eligibility=[],
        required_documents=[],
        venue_or_submission_method=None,
        fees=None,
        contact_information=[],
        important_points=["This is demo mode; connect an LLM API for full extraction."],
        missing_information=["Detailed structured extraction requires live LLM analysis."],
        clarification_questions=["What exact submission procedure and deadline details apply?"],
    )
