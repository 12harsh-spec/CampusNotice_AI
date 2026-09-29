import json
import streamlit as st

from src.config import get_settings
from src.analyzer import analyze_notice
from src.prompt_loader import load_prompt

st.set_page_config(
    page_title="CampusNotice AI",
    page_icon="🎓",
    layout="wide",
)

SAMPLE_NOTICE = """NOTICE — Internship Opportunity for Semester V Students

The Training and Placement Cell is pleased to announce that applications are invited for the Summer Industry Internship Programme 2027. Students currently enrolled in Semester V of B.Tech are eligible to apply.

Interested students must submit their updated resume, college ID card, and a passport-size photograph through the internship registration form on or before 5 October 2026.

The internship will commence from 1 December 2026 and will be conducted at the partner company's Jaipur office. Students are advised to register before the deadline.

For queries, contact the Training and Placement Cell at tpo@college.edu."""

settings = get_settings()

st.title("🎓 CampusNotice AI")
st.caption("NLP + LLM system for turning college notices into student action briefs")

with st.sidebar:
    st.header("Project Configuration")
    st.write(f"**Model:** `{settings.model}`")
    st.write(f"**Temperature:** `{settings.temperature}`")
    st.write(f"**Max tokens:** `{settings.max_output_tokens}`")
    st.write(
        "**Mode:** " +
        ("Demo / Mock" if settings.demo_mode or not settings.api_key else "Live LLM API")
    )
    st.info("The API key is loaded from an environment variable and is never shown.")

tab_analyze, tab_pipeline, tab_evaluation = st.tabs(
    ["📝 Analyze Notice", "🧠 NLP Pipeline", "📊 Evaluation"]
)

with tab_analyze:
    st.subheader("Paste a college notice")

    notice = st.text_area(
        "Notice text",
        value=SAMPLE_NOTICE,
        height=260,
        help="Paste the complete notice for best extraction accuracy.",
    )

    c1, c2 = st.columns([1, 1])
    with c1:
        analyze = st.button("Analyze Notice", type="primary", use_container_width=True)
    with c2:
        if st.button("Reset to Sample", use_container_width=True):
            st.rerun()

    if analyze:
        if not notice.strip():
            st.warning("Please enter a college notice.")
        else:
            with st.spinner("Extracting notice information..."):
                try:
                    result, features = analyze_notice(notice, settings)
                    st.session_state["result"] = result
                    st.session_state["features"] = features
                except Exception as exc:
                    st.error(f"Analysis failed: {exc}")

    if "result" in st.session_state:
        result = st.session_state["result"]
        features = st.session_state["features"]

        st.divider()
        st.subheader("Student Action Brief")

        m1, m2, m3 = st.columns(3)
        m1.metric("Category", result.notice_category)
        m2.metric("Deadline", result.deadline or "Not specified")
        m3.metric("Actions", len(result.action_required))

        st.markdown(f"## {result.title}")
        st.write(result.summary)

        left, right = st.columns(2)

        with left:
            st.markdown("### ✅ What you need to do")
            if result.action_required:
                for item in result.action_required:
                    st.write(f"• {item}")
            else:
                st.write("No explicit action extracted.")

            st.markdown("### 👥 Eligibility")
            for item in result.eligibility or ["Not specified"]:
                st.write(f"• {item}")

            st.markdown("### 📄 Required Documents")
            for item in result.required_documents or ["Not specified"]:
                st.write(f"• {item}")

            st.markdown("### 💰 Fees")
            st.write(result.fees or "Not specified")

        with right:
            st.markdown("### 📍 Venue / Submission")
            st.write(result.venue_or_submission_method or "Not specified")

            st.markdown("### 📞 Contact")
            for item in result.contact_information or ["Not specified"]:
                st.write(f"• {item}")

            st.markdown("### ⭐ Important Points")
            for item in result.important_points or ["None extracted"]:
                st.write(f"• {item}")

            st.markdown("### ⚠ Missing Information")
            for item in result.missing_information or ["No obvious missing information identified"]:
                st.write(f"• {item}")

        st.markdown("### ❓ Clarification Questions")
        for item in result.clarification_questions or ["No clarification questions generated."]:
            st.write(f"• {item}")

        with st.expander("Original Notice"):
            st.text(notice)

        with st.expander("Structured JSON"):
            st.json(result.model_dump())

        st.download_button(
            "Download JSON",
            data=json.dumps(result.model_dump(), indent=2),
            file_name="campusnotice_analysis.json",
            mime="application/json",
        )

        st.caption(f"Basic preprocessing features: {features}")

        st.warning(
            "CampusNotice AI summarizes and extracts information from notices. "
            "Always verify official deadlines and instructions against the original notice."
        )

with tab_pipeline:
    st.subheader("How the NLP + LLM pipeline works")

    stages = [
        ("1", "Preprocessing", "Normalize whitespace and calculate basic linguistic signals."),
        ("2", "Classification", "Identify whether the notice concerns an exam, internship, placement, scholarship, event, etc."),
        ("3", "Information Extraction", "Extract dates, eligibility, documents, fees, contacts, venue, and actions."),
        ("4", "Prompt Construction", "Insert the cleaned notice into the version-controlled prompt."),
        ("5", "LLM API", "Ask the LLM for structured JSON rather than free-form text."),
        ("6", "Validation", "Validate the response against a Pydantic schema."),
        ("7", "Student Brief", "Present the extracted information in a readable format."),
    ]

    for number, title, description in stages:
        st.markdown(f"### {number}. {title}")
        st.write(description)

    st.subheader("Prompt Strategy")
    st.write(
        "The prompt is stored separately in `prompts/notice_analysis.txt`. "
        "It defines the output schema, prevents invented facts, requires missing-information detection, "
        "and forces JSON-only output."
    )

    if st.button("Preview prompt template"):
        preview = load_prompt("{NOTICE_TEXT}")
        st.code(preview, language="text")

with tab_evaluation:
    st.subheader("Evaluation Dataset")
    st.write(
        "Five realistic notice categories are included. The structural evaluation checks whether "
        "all required fields are represented in a validated model."
    )

    try:
        from src.evaluation import load_cases, REQUIRED_FIELDS
        cases = load_cases()

        for case in cases:
            st.markdown(f"**Case {case['id']} — {case['category']}**")
            st.caption(case["notice"])

        st.divider()
        st.metric("Evaluation Cases", len(cases))
        st.metric("Required Output Fields", len(REQUIRED_FIELDS))
        st.info("Run `pytest` for unit tests and `python -m src.evaluation` for the evaluation summary.")
    except Exception as exc:
        st.error(str(exc))
