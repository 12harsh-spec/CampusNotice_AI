import json
from openai import OpenAI
from .config import Settings
from .models import NoticeAnalysis

class LLMClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = OpenAI(api_key=settings.api_key)

    def analyze(self, prompt: str) -> NoticeAnalysis:
        response = self.client.chat.completions.create(
            model=self.settings.model,
            temperature=self.settings.temperature,
            max_tokens=self.settings.max_output_tokens,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "Return only valid JSON matching the requested schema."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )

        content = response.choices[0].message.content or "{}"
        data = json.loads(content)
        return NoticeAnalysis.model_validate(data)
