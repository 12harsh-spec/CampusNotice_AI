# CampusNotice AI — College Notice Intelligence System

## NLP Project Submission

**Submission type:** Solo NLP + LLM API project

CampusNotice AI converts long, formal college notices into concise, structured student action briefs.

### Problem Statement

College notices often contain important information about deadlines, eligibility, required documents, fees, venues, and actions. Because notices are written in formal language, students may miss critical details.

CampusNotice AI applies NLP preprocessing and an LLM API to transform an unstructured notice into structured information.

### Core Pipeline

```text
College Notice
      ↓
Text Preprocessing
      ↓
Basic NLP Feature Extraction
      ↓
Notice Classification
      ↓
Prompt Construction
      ↓
LLM API
      ↓
Structured JSON
      ↓
Pydantic Validation
      ↓
Student Action Brief
```

### LLM Usage

The LLM is used meaningfully for:

- Notice category understanding
- Information extraction
- Action extraction
- Deadline and date interpretation
- Eligibility extraction
- Missing-information detection
- Student-friendly summarization
- Generation of clarification questions

The model is instructed not to invent information.

## Project Structure

```text
CampusNotice_AI/
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── config/
│   └── config.example.json
│
├── prompts/
│   └── notice_analysis.txt
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── preprocessing.py
│   ├── prompt_loader.py
│   ├── llm_client.py
│   ├── analyzer.py
│   └── evaluation.py
│
├── data/
│   └── sample_notices.json
│
└── tests/
    └── test_pipeline.py
```

## Installation

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the API

Copy:

```text
.env.example → .env
```

Then add your API key:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.2
OPENAI_MAX_OUTPUT_TOKENS=1200
DEMO_MODE=false
```

Never commit `.env` to GitHub.

### 4. Run

```bash
streamlit run app.py
```

The project can also run in demo mode without an API key:

```env
DEMO_MODE=true
```

## NLP Techniques

### 1. Text preprocessing

Whitespace normalization and basic text cleanup are performed before analysis.

### 2. Notice classification

The system identifies categories such as:

- Internship
- Exam
- Scholarship
- Placement
- Event
- Administrative
- Fee
- Admission
- Other

### 3. Information extraction

The system extracts:

- Notice title
- Deadline
- Eligibility
- Required documents
- Fees
- Venue/submission method
- Contact information
- Important points

### 4. Action extraction

The LLM identifies what the student is actually expected to do.

### 5. Missing-information detection

Rather than guessing, the system explicitly reports information that is not present.

### 6. Structured LLM output

The LLM returns JSON which is validated using Pydantic.

## Prompt Engineering

The prompt is intentionally stored separately in:

```text
prompts/notice_analysis.txt
```

The prompt:

- defines the role
- defines the exact output schema
- prohibits hallucination
- separates facts from questions
- requires missing information to be identified
- requires JSON-only output
- defines allowed categories
- instructs the model to preserve dates exactly
- prioritizes concise student-friendly language

This makes the prompt easy to test, version, and improve independently from the Python application.

## Evaluation

The project includes five evaluation cases:

1. Internship notice
2. Examination notice
3. Scholarship notice
4. Placement notice
5. College event notice

The evaluation checks structural completeness of the generated result.

Run:

```bash
python -m src.evaluation
```

Run tests:

```bash
pytest
```

The structural score measures whether required output fields are present. It is not a claim that an LLM is always factually correct.

## API Efficiency

The implementation:

- sends one LLM request per notice
- keeps the prompt external and reusable
- uses structured JSON output
- limits output tokens
- uses a low temperature for consistent extraction
- validates the result before displaying it
- supports demo mode to avoid unnecessary API calls

## Limitations

The application depends on the quality of the original notice. It should not be treated as the official source of deadlines or instructions.

Students should always verify important information against the original college notice.

## Teacher Evaluation Mapping

| Evaluation Criterion | Implementation |
|---|---|
| Quality and efficiency of code | Modular Python architecture, validation, error handling, tests |
| LLM API functionality | OpenAI API integration in `llm_client.py` |
| Prompt effectiveness | Dedicated structured prompt in `prompts/notice_analysis.txt` |
| Overall project quality | Streamlit interface, evaluation dataset, documentation, demo mode |
