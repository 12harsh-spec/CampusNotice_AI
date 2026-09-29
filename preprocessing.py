import re

def normalize_notice(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text

def extract_basic_features(text: str) -> dict:
    lowered = text.lower()
    return {
        "word_count": len(text.split()),
        "character_count": len(text),
        "contains_deadline_language": any(
            x in lowered for x in ["deadline", "on or before", "last date", "due date", "submit by"]
        ),
        "contains_contact_language": any(
            x in lowered for x in ["contact", "email", "phone", "office"]
        ),
    }
