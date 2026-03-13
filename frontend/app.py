import streamlit as st
import requests

st.title("AI Contract Analyzer")

uploaded = st.file_uploader("Upload Contract")

if uploaded:

    files = {"file": uploaded.getvalue()}

    r = requests.post("http://localhost:8000/upload", files={"file": uploaded})

    result = r.json()

    st.subheader("Risk Analysis")

    for item in result["analysis"]:

        st.write("Clause:")
        st.write(item["clause"])

        st.write("Risk:", item["risk"])
        st.write("---")


query = st.text_input("Search Contract")

if st.button("Search"):

    r = requests.get("http://localhost:8000/search", params={"query": query})

    for res in r.json()["results"]:
        st.write(res)