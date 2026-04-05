import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Contract Analyzer", layout="wide")
st.title("AI Contract Analyzer")

# ── Upload Section ──────────────────────────────────────────
uploaded = st.file_uploader("Upload a contract (PDF or DOCX)", type=["pdf", "docx"])

if uploaded:
    with st.spinner("Analyzing contract... this may take a minute"):
        r = requests.post(
            f"{BASE_URL}/upload",
            files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
        )

    if r.status_code != 200:
        st.error(f"Backend error: {r.status_code} — {r.text}")
    else:
        result = r.json()

        # ── Contract-level LLM Summary ───────────────────────
        st.subheader("Contract Summary")
        st.write(result.get("llm_contract_analysis", "No summary available."))

        # ── Obligations ──────────────────────────────────────
        st.subheader("Obligations")
        obligations = result.get("obligations", {})
        if isinstance(obligations, dict):
            st.write("**LLM Extraction:**")
            st.write(obligations.get("llm_extraction", ""))
            st.write("**Keyword Matches:**")
            for o in obligations.get("keyword_matches", []):
                st.write(f"- {o}")
        else:
            for o in obligations:
                st.write(f"- {o}")

        # ── Clause Risk Analysis ─────────────────────────────
        st.subheader("Clause Risk Analysis")
        for item in result.get("analysis", []):
            risk = item["risk"]
            color = "🔴" if risk == "High Risk" else "🟢"
            with st.expander(f"{color} {risk} — {item['clause'][:80]}..."):
                st.write(item["clause"])

        # ── LLM Clause Analysis ──────────────────────────────
        st.subheader("LLM Clause Analysis")
        for item in result.get("llm_clause_analysis", []):
            with st.expander(f"Clause: {item['clause'][:80]}..."):
                st.write(item["analysis"])

# ── Search Section ───────────────────────────────────────────
st.divider()
st.subheader("Search Contract")

query = st.text_input("Ask a question about the contract")

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a search query.")
    else:
        with st.spinner("Searching..."):
            r = requests.get(f"{BASE_URL}/search", params={"query": query})

        if r.status_code != 200:
            st.error(f"Search error: {r.status_code} — {r.text}")
        else:
            data = r.json()

            st.write("**Answer:**")
            st.write(data.get("answer", "No answer returned."))

            st.write("**Relevant Clauses:**")