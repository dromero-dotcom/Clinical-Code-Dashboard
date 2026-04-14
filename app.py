import streamlit as st
import json
import os

st.set_page_config(page_title="NICE Clinical Code Review", layout="wide")

# 1. Load Data with Session State
def load_data():
    if 'audit_data' not in st.session_state:
        if os.path.exists('audit_trail.json'):
            with open('audit_trail.json', 'r') as f:
                st.session_state.audit_data = json.load(f)
        else:
            st.session_state.audit_data = []

load_data()

# 2. App Header
st.title("🩺 NICE Clinical Code Review Dashboard")
st.markdown("""
Review the AI-suggested clinical codes below. Use the **Approve** or **Reject** buttons to build the version-controlled final dataset.
""")

st.divider()

# 3. Sidebar Metrics
total_codes = len(st.session_state.audit_data)
approved = sum(1 for x in st.session_state.audit_data if x['status'] == 'Approved')
rejected = sum(1 for x in st.session_state.audit_data if x['status'] == 'Rejected')
pending = sum(1 for x in st.session_state.audit_data if x['status'] == 'Pending')

with st.sidebar:
    st.header("Review Progress")
    st.write(f"Total codes: {total_codes}")
    st.write(f"Approved ✅: {approved}")
    st.write(f"Rejected ❌: {rejected}")
    st.write(f"Pending ⏳: {pending}")

if st.sidebar.button("💾 Save & Finalize Decisions"):
    with open('audit_trail.json', 'w') as f:
        json.dump(st.session_state.audit_data, f, indent=4)
    st.sidebar.success("Saved to JSON successfully!")

# 4. Main Interface - Displaying the Codes
for index, item in enumerate(st.session_state.audit_data):
    # Use standard markdown coloring via text status for highlighting ambiguity
    bg_color = "#fff8e6" if item['Is_Ambiguous'] else "#ffffff"

    with st.container():
        # Using columns to lay out the row
        col1, col2, col3 = st.columns([1, 4, 1.5])

        with col1:
            st.subheader(f"SNOMED Code: {item['SNOMED_Code']}")
            # Status badge
            if item['status'] == 'Approved':
                st.success("Approved")
            elif item['status'] == 'Rejected':
                st.error("Rejected")
            else:
                st.warning("Pending")

        with col2:
            st.markdown(f"**Description:** {item['Matched_Description']}")
            #st.markdown(f"**AI Rationale (Audit Trail):** {item['rationale']}")
            st.caption(f"Confidence Score: {item['Confidence_score']}")

            if item['Is_Ambiguous']:
                st.markdown("⚠️ **AI Marked this as Ambiguous.** Human review highly recommended.")

           # Analyst notes
            notes = st.text_input(
                "Analyst Notes / Rationale for Override",
                value=item['analyst_notes'],
                key=f"notes_{index}"
            )
            st.session_state.audit_data[index]['analyst_notes'] = notes

        with col3:
            st.write("") # Spacer
            st.write("") # Spacer

            # Action buttons
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("Approve", key=f"app_{index}", use_container_width=True):
                    st.session_state.audit_data[index]['status'] = 'Approved'
                    st.rerun()
            with btn_col2:
                if st.button("Reject", key=f"rej_{index}", use_container_width=True):
                    st.session_state.audit_data[index]['status'] = 'Rejected'
                    st.rerun()

        st.divider()
