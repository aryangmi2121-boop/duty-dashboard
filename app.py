import streamlit as st
import pandas as pd

st.title("🚆 Duty Management Dashboard")

# storage
if "roster" not in st.session_state:
    st.session_state.roster = []

# options
employees = ["Aryan", "John", "Ravi", "Neha", "Sanya"]
departments = ["Vande Bharat & CCTV", "Central Control"]
shifts = ["Morning (06-14)", "General (12-20)", "Night (22-06)"]
leave_types = ["None", "CR", "CL", "NH", "PL", "Leave"]

# UI
date = st.date_input("Date")
dept = st.selectbox("Department", departments)
emp = st.selectbox("Employee", employees)
shift = st.selectbox("Shift", shifts)
leave = st.selectbox("Leave", leave_types)

# buttons
col1, col2 = st.columns(2)

if col1.button("➕ Add Duty"):
    st.session_state.roster.append({
        "Date": str(date),
        "Department": dept,
        "Employee": emp,
        "Shift": shift,
        "Leave": leave
    })
    st.success("Duty Added!")

if col2.button("🗑 Clear"):
    st.session_state.roster = []

# table
st.subheader("📋 Roster")
st.dataframe(pd.DataFrame(st.session_state.roster))
