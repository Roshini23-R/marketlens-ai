import json

from google import genai
from google.genai import types

from app.agents.state import ResearchState
from app.config import GEMINI_API_KEY


def report_synthesizer_node(state: ResearchState) -> dict:
    company = state["company"]
    focus = state["focus"]
    competitors = state.get("competitors", [])
    sources = state.get("sources", [])

    competitor_text = (
        ", ".join(competitors)
        if competitors
        else "No direct competitors supplied"
    )

    source_blocks = []

    for number, source in enumerate(sources, start=1):
        source_blocks.append(
            f"""[{number}]
Title: {source.get("title", "Untitled source")}
URL: {source.get("url", "")}
Snippet: {source.get("snippet", "")}"""
        )

    sources_text = (
        "\n\n".join(source_blocks)
        if source_blocks
        else "No usable public sources were retrieved."
    )

    prompt = f"""
You are a careful competitive-intelligence analyst.

Company: {company}
Research focus: {focus}
Competitors: {competitor_text}

Numbered public-source excerpts:
{sources_text}

Rules:
1. Use only the supplied source titles and snippets.
2. Do not invent prices, features, market share, rankings, customers, or facts.
3. If evidence is missing, write exactly:
   "Insufficient evidence in the provided sources."
4. Do not claim that any information is verified.
5. Keep the output neutral, concise, and useful for product and marketing teams.
6. Refer only to supplied source numbers, such as [1], [2], and [3].
7. Return only valid JSON.
8. Do not return Markdown code fences or explanations.

Return this exact JSON structure:
{{
  "executive_summary": "string",
  "key_findings": ["string"],
  "competitor_comparison": ["string"],
  "swot": {{
    "strengths": ["string"],
    "weaknesses": ["string"],
    "opportunities": ["string"],
    "threats": ["string"]
  }},
  "evidence_gaps": ["string"],
  "limitations": "string"
}}
"""

    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured")

    client = genai.Client(
        api_key=GEMINI_API_KEY,
        
            )
   

    try:
        gemini_response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2,
            ),
        )

        report_text = gemini_response.text

        if not report_text:
            raise RuntimeError("Gemini returned an empty response")

        report = json.loads(report_text)

        required_sections = [
            "executive_summary",
            "key_findings",
            "competitor_comparison",
            "swot",
            "evidence_gaps",
            "limitations",
        ]

        missing_sections = [
            section
            for section in required_sections
            if section not in report
        ]

        if missing_sections:
            raise RuntimeError(
                f"Gemini report is missing sections: {missing_sections}"
            )

        if not report.get("executive_summary"):
            raise RuntimeError(
                "Gemini returned a report without an executive summary"
            )

    except Exception:
        report = {
            "executive_summary": (
                "Automated report synthesis is temporarily unavailable. "
                "The retrieved public sources below can still be reviewed "
                "for pricing, product, and competitor evidence."
            ),
            "key_findings": [],
            "competitor_comparison": [],
            "swot": {
                "strengths": [],
                "weaknesses": [],
                "opportunities": [],
                "threats": [],
            },
            "evidence_gaps": [
                "Automated synthesis was unavailable for this run."
            ],
            "limitations": (
                "This run returned source-backed search results but could "
                "not complete Gemini report synthesis because the model "
                "service was temporarily unavailable."
            ),
        }

    return {
        "report": report,
        "summary": report["executive_summary"],
    }