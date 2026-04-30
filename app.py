import streamlit as st
import pandas as pd

st.set_page_config(page_title="Duty Dashboard", layout="wide")

st.title("🚆 Duty Management Dashboard")

# ---------------- DATA ----------------
departments = ["Vande Bharat & CCTV", "Central Control"]

shifts = [
    "06-14", "08-16", "09-17",
    "10-18", "12-20", "14-22",
    "17-09 (16hr)"
]

status_types = ["Duty", "CR", "CL", "NH", "Leave", "Rest"]

# ---------------- SESSION STORAGE ----------------
if "roster" not in st.session_state:
    st.session_state.roster = []

# ---------------- INPUT UI ----------------
col1, col2, col3 = st.columns(3)

with col1:
    date = st.date_input("Date")
    department = st.selectbox("Department", departments)

with col2:
    employee = st.text_input("Employee Name")
    shift = st.selectbox("Shift", shifts)

with col3:
    status = st.selectbox("Status", status_types)

# ---------------- CONFLICT CHECK ----------------
def
