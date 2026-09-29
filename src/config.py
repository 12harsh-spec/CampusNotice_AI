import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    api_key: str
    model: str
    temperature: float
    max_output_tokens: int
    demo_mode: bool

def get_settings() -> Settings:
    return Settings(
        api_key=os.getenv("OPENAI_API_KEY", ""),
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.2")),
        max_output_tokens=int(os.getenv("OPENAI_MAX_OUTPUT_TOKENS", "1200")),
        demo_mode=os.getenv("DEMO_MODE", "true").lower() == "true",
    )
