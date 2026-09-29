from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT_PATH = ROOT / "prompts" / "notice_analysis.txt"

def load_prompt(notice: str) -> str:
    template = PROMPT_PATH.read_text(encoding="utf-8")
    template = template.replace("{notice}", notice)
    return template
