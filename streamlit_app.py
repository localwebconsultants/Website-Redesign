
import streamlit as st
from app.analyze import analyze_website
import pandas as pd
import os

st.set_page_config(layout="wide")
st.title("🔍 Website Design Quality Checker")

url_input = st.text_input("Enter a website URL to analyze:")

if url_input:
    result = analyze_website(url_input)

    # Screenshot feature disabled for Streamlit Cloud
    # take_screenshot(url_input)

    st.write(f"**Design Score:** {result['score']} / 100")
    st.write(f"**Load Time:** {result['load_time']} seconds")
    st.write("### Issues Detected:")
    for issue in result["issues"]:
        st.markdown(f"- {issue}")

    df = pd.DataFrame([{
        "URL": result["url"],
        "Score": result["score"],
        "Load Time": result["load_time"],
        "Issues": "; ".join(result["issues"])
    }])
    st.download_button("📥 Download Report CSV", df.to_csv(index=False), "design_report.csv", "text/csv")

st.markdown("---")
st.subheader("📄 Batch Processing")
uploaded_file = st.file_uploader("Upload a CSV file with a column named 'url':", type="csv")

if uploaded_file:
    urls_df = pd.read_csv(uploaded_file)
    results = []

    for url in urls_df["url"]:
        result = analyze_website(url)
        results.append({
            "URL": result["url"],
            "Score": result["score"],
            "Load Time": result["load_time"],
            "Issues": "; ".join(result["issues"])
        })

    results_df = pd.DataFrame(results)
    st.dataframe(results_df)
    st.download_button("📥 Download Batch Report", results_df.to_csv(index=False), "batch_report.csv", "text/csv")
