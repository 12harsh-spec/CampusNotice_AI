from src.preprocessing import normalize_notice, extract_basic_features
from src.models import NoticeAnalysis
from src.evaluation import structural_score

def test_normalization():
    assert normalize_notice("  Hello   college   students ") == "Hello college students"

def test_basic_features():
    result = extract_basic_features(
        "Submit the form on or before the deadline. Contact the office."
    )
    assert result["word_count"] > 0
    assert result["contains_deadline_language"] is True
    assert result["contains_contact_language"] is True

def test_schema():
    result = NoticeAnalysis(
        notice_category="Internship",
        title="Internship",
        summary="Apply for internship.",
        action_required=["Apply"],
    )
    assert structural_score(result) == 1.0
