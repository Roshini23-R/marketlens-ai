import os

import requests
import streamlit as st

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://marketlens-ai-op67.onrender.com",
)

st.set_page_config(
    page_title="MarketLens AI",
    page_icon="🔍",
    layout="wide",
)

st.title("MarketLens AI")
st.caption(
    "Source-backed competitive intelligence for product and marketing teams."
)

st.info(
    "Enter a company, a research focus, and optional competitors. "
    "MarketLens AI retrieves public sources and generates a concise "
    "competitive research brief."
)

with st.form("research_form"):
    company = st.text_input(
        "Company",
        value="Zoho",
        placeholder="Example: Zoho",
    )

    focus = st.text_input(
        "Research focus",
        value="product differentiation and pricing",
        placeholder="Example: pricing, product differentiation, target market",
    )

    competitors_text = st.text_input(
        "Competitors (comma-separated)",
        value="Freshworks",
        placeholder="Example: Freshworks, Salesforce",
    )

    submitted = st.form_submit_button(
        "Run research",
        use_container_width=True,
    )

if submitted:
    if not company.strip():
        st.error("Please enter a company name.")
        st.stop()

    if not focus.strip():
        st.error("Please enter a research focus.")
        st.stop()

    competitors = [
        item.strip()
        for item in competitors_text.split(",")
        if item.strip()
    ]

    payload = {
        "company": company.strip(),
        "focus": focus.strip(),
        "competitors": competitors,
    }

    with st.spinner("Researching public sources..."):
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/v1/research/",
                json=payload,
                timeout=120,
            )
            response.raise_for_status()
            data = response.json()

        except requests.Timeout:
            st.error(
                "The request took too long. The public backend may be "
                "waking up or the AI service may be busy. Please try again."
            )
            st.stop()

        except requests.RequestException as exc:
            st.error(
                "Unable to reach the research service. Please try again "
                "in a moment."
            )
            st.caption(f"Technical detail: {exc}")
            st.stop()

    st.success("Research complete")

    st.subheader("Executive summary")
    st.write(data.get("summary", "No summary was returned."))

    report = data.get("report", {})

    if report:
        key_findings = report.get("key_findings", [])

        if key_findings:
            st.subheader("Key findings")

            for finding in key_findings:
                st.write(f"- {finding}")

        comparison = report.get("competitor_comparison", [])

        if comparison:
            st.subheader("Competitor comparison")

            for item in comparison:
                st.write(f"- {item}")

        swot = report.get("swot", {})

        if swot:
            st.subheader("SWOT analysis")

            columns = st.columns(4)

            sections = [
                ("Strengths", "strengths"),
                ("Weaknesses", "weaknesses"),
                ("Opportunities", "opportunities"),
                ("Threats", "threats"),
            ]

            for column, (label, key) in zip(columns, sections):
                with column:
                    st.markdown(f"**{label}**")

                    items = swot.get(key, [])

                    if items:
                        for item in items:
                            st.write(f"- {item}")
                    else:
                        st.caption("Insufficient evidence in the provided sources.")

        evidence_gaps = report.get("evidence_gaps", [])

        if evidence_gaps:
            st.subheader("Evidence gaps")

            for gap in evidence_gaps:
                st.write(f"- {gap}")

        limitations = report.get("limitations")

        if limitations:
            st.subheader("Limitations")
            st.warning(limitations)

    st.subheader("Public sources")

    sources = data.get("sources", [])

    if sources:
        for number, source in enumerate(sources, start=1):
            title = source.get("title", "Untitled source")
            url = source.get("url", "")
            snippet = source.get("snippet", "")

            st.markdown(f"### [{number}. {title}]({url})")

            if snippet:
                st.write(snippet)
    else:
        st.info("No public sources were returned for this research run.")

st.divider()

st.caption(
    "MarketLens AI uses public web-source excerpts for exploratory research. "
    "Review source links and validate important claims before making "
    "business decisions."
)