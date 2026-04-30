import streamlit as st
import pandas as pd

st.set_page_config(page_title="Duty Dashboard", layout="wide")
st.title("🚆 Duty Management Dashboard")

departments = ["Vande Bharat & CCTV", "Central Control"]

shifts = [
    "06-14","08-16","09-17","10-18",
    "12-20","14-22","17-09 (16hr)"
]

leave_types = ["None","CR","CL","NH","Leave","Rest"]

if "roster" not in st.session_state:
    st.session_state.roster = []

# INPUT
c1, c2, c3 = st.columns(3)

with c1:
    date = st.date_input("Date")
    department = st.selectbox("Department", departments)

with c2:
    employee = st.text_input("Employee Name")
    shift = st.selectbox("Shift", shifts)

with c3:
    leave = st.selectbox("Leave", leave_types)

# CONFLICT
def check_conflict(date, employee, leave):
    for row in st.session_state.roster:
        if row["Date"] == str(date) and row["Employee"].lower() == employee.lower():
            return "Employee already assigned on this date!"
        if leave != "None":
            return f"Employee is on {leave}, cannot assign duty!"
    return None

# ASSIGN
if st.button("Assign Duty"):
    if employee.strip() == "":
        st.warning("Enter employee name")
    else:
        conflict = check_conflict(date, employee, leave)
        if conflict:
            st.error(conflict)
        else:
            st.session_state.roster.append({
                "Date": str(date),
                "Department": department,
                "Employee": employee,
                "Shift": shift,
                "Leave": leave
            })
            st.success("Duty Assigned")

# TABLE
st.subheader("📋 Roster")
df = pd.DataFrame(st.session_state.roster)
st.dataframe(df, use_container_width=True)

# DOWNLOAD
if len(st.session_state.roster) > 0:
    st.download_button(
        "📥 Download Excel",
        df.to_csv(index=False),
        file_name="roster.csv",
        mime="text/csv"
    )

