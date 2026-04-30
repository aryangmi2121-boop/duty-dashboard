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
def check_conflict(date, employee):
    for row in st.session_state.roster:
        if row["Date"] == str(date) and row["Employee"].lower() == employee.lower():
            return "🚨 Already assigned for this date!"
    return None

# ---------------- ASSIGN DUTY ----------------
if st.button("Assign Duty"):
    if employee.strip() == "":
        st.warning("Enter employee name")
    else:
        conflict = check_conflict(date, employee)

        if conflict:
            st.error(conflict)
        else:
            st.session_state.roster.append({
                "Date": str(date),
                "Department": department,
                "Employee": employee,
                "Shift": shift,
                "Status": status
            })
            st.success("✅ Saved")

# ---------------- DATAFRAME ----------------
df = pd.DataFrame(st.session_state.roster)

# ---------------- DISPLAY SECTIONS ----------------
if not df.empty:

    st.subheader("📋 Vande Bharat & CCTV")
    st.dataframe(
        df[df["Department"] == "Vande Bharat & CCTV"],
        use_container_width=True
    )

    st.subheader("📋 Central Control")
    st.dataframe(
        df[df["Department"] == "Central Control"],
        use_container_width=True
    )

    # ---------------- SWAP FEATURE ----------------
    st.markdown("### 🔄 Swap Employee")

    idx = st.number_input(
        "Row Index",
        min_value=0,
        max_value=len(df)-1
    )

    new_emp = st.text_input("New Employee Name")

    if st.button("Swap"):
        if new_emp.strip():
            st.session_state.roster[idx]["Employee"] = new_emp
            st.success("✅ Swapped")
            st.rerun()

    # ---------------- DELETE FEATURE ----------------
    st.markdown("### 🗑️ Delete Row")

    del_idx = st.number_input(
        "Delete Index",
        min_value=0,
        max_value=len(df)-1
    )

    if st.button("Delete"):
        st.session_state.roster.pop(del_idx)
        st.success("Deleted")
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

    # ---------------- SINGLE FULL DOWNLOAD ----------------
    st.markdown("### 📥 Download Complete Roster")

    final_df = pd.DataFrame(st.session_state.roster)
    final_df = final_df.sort_values(by=["Date", "Department", "Shift"])

    st.download_button(
        "📥 Download FULL Roster (Single Sheet)",
        final_df.to_csv(index=False),
        file_name="complete_roster.csv",
        mime="text/csv"
    )

else:
    st.info("No data yet")
