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

leave_types = ["None", "CR", "CL", "NH", "Leave", "Rest"]

# ---------------- SESSION ----------------
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
    leave = st.selectbox("Leave", leave_types)

# ---------------- CONFLICT CHECK ----------------
def check_conflict(date, employee, leave):
    for row in st.session_state.roster:
        if row["Date"] == str(date) and row["Employee"].lower() == employee.lower():
            return "🚨 Employee already assigned on this date!"
        if leave != "None":
            return f"🚨 Employee marked {leave}, cannot assign duty!"
    return None

# ---------------- ASSIGN ----------------
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
            st.success("✅ Duty Assigned")

# ---------------- ROSTER ----------------
st.subheader("📋 Roster")

df = pd.DataFrame(st.session_state.roster)

if not df.empty:
    st.dataframe(df, use_container_width=True)

    # ---------------- SWAP SYSTEM ----------------
    st.markdown("### 🔄 Swap Duty (Replace Employee)")

    idx = st.number_input("Row Index to Replace", min_value=0, max_value=len(df)-1 if len(df)>0 else 0)

    new_emp = st.text_input("New Employee Name")

    if st.button("Swap Duty"):
        if new_emp.strip() != "":
            st.session_state.roster[idx]["Employee"] = new_emp
            st.success("✅ Duty Swapped")
            st.rerun()

    # ---------------- CALENDAR VIEW ----------------
    st.markdown("### 📅 Calendar View")

    cal = df.pivot_table(
        index="Date",
        columns="Shift",
        values="Employee",
        aggfunc="first"
    )

    st.dataframe(cal, use_container_width=True)

else:
    st.info("No roster yet")

# ---------------- DOWNLOAD ----------------
if not df.empty:
    st.download_button(
        "📥 Download Excel",
        df.to_csv(index=False),
        file_name="roster.csv",
        mime="text/csv"
    )
