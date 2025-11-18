%%writefile team_tracker.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Dozee Team Performance Tracker", layout="wide")

st.title("📊 Dozee Team Daily Performance Tracker")

DATA_FILE = "team_data.csv"

# Load existing saved data
if os.path.exists(DATA_FILE):
    st.session_state.data = pd.read_csv(DATA_FILE)
else:
    if "data" not in st.session_state:
        st.session_state.data = pd.DataFrame(columns=["Date","Name","Task","Status","Hours","Efficiency"])

# --------------- FORM FOR NEW ENTRY ----------------
with st.form("task_form"):
    st.subheader("➕ Add Team Update")

    name = st.text_input("Team Member Name")
    task = st.text_input("Task Description")
    status = st.selectbox("Task Status", ["In Progress", "Completed", "Blocked"])
    hours = st.number_input("Hours Spent", min_value=0.0, step=0.5)
    estimated = st.number_input("Estimated Hours", min_value=0.5, step=0.5)
    submit = st.form_submit_button("Add Entry")

if submit:
    efficiency = round((estimated / hours) * 100, 2) if hours > 0 else 0
    new_entry = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Name": name,
        "Task": task,
        "Status": status,
        "Hours": hours,
        "Efficiency": efficiency
    }
    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_entry])], ignore_index=True)
    st.session_state.data.to_csv(DATA_FILE, index=False)

# --------------- DASHBOARD ----------------
st.divider()
st.subheader("📌 Team Dashboard")

if len(st.session_state.data) > 0:
    for i, row in st.session_state.data.iterrows():
        with st.expander(f"{row['Name']} - {row['Task']}"):
            st.write(f"📅 **Date:** {row['Date']}")
            st.write(f"📝 **Task:** {row['Task']}")
            st.write(f"📌 **Status:** {row['Status']}")
            st.write(f"⏱ **Hours Spent:** {row['Hours']}")
            st.write(f"⚡ **Efficiency:** {row['Efficiency']}%")
            if st.button("❌ Delete Entry", key=f"delete_{i}"):
                st.session_state.data = st.session_state.data.drop(i).reset_index(drop=True)
                st.session_state.data.to_csv(DATA_FILE, index=False)
                st.rerun()

    st.subheader("📈 Summary Metrics")
    st.metric("Average Efficiency", f"{round(st.session_state.data['Efficiency'].mean(),2)}%")

    csv = st.session_state.data.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Download CSV Report", csv, "team_report.csv", "text/csv")

else:
    st.info("No records found. Add updates above.")
