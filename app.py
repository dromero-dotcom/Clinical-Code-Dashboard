import streamlit as st
#import json
#import os

st.set_page_config(page_title="NICE Clinical Code Review", layout="wide")

st.title("🩺 NICE Clinical Code Review Dashboard")
st.markdown("""
Review the AI-suggested clinical codes below. Use the **Approve** or **Reject** buttons to build the version-controlled final dataset.
""")
st.write("Hello! This is where the SNOMED Codes and descriptions would be shown!")

st.divider()


# Sidebar Metrics
total_codes = 5
approved = 0 
rejected = 0
pending = 5

with st.sidebar:
    st.header("Review Progress")
    st.write(f"Total codes: {total_codes}")
    st.write(f"Approved ✅: {approved}")
    st.write(f"Rejected ❌: {rejected}")
    st.write(f"Pending ⏳: {pending}")
