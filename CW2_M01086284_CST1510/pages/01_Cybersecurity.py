#-------------------------required connections-------------------------------

import streamlit as st
import pandas as pd
from datetime import datetime
from app.data.incidents import CyberIncidentManager
from gemini_basic import AIQueryManager

ai=AIQueryManager()

incident_manager = CyberIncidentManager()

#-----------------------------cybersecurity dashboard------------------------------------

def cybersecurity_page():
    st.title("🛡️ Cybersecurity Dashboard")

    df = incident_manager.get_all_incidents()
    st.subheader("🚨Cyber Incidents Table")
    st.dataframe(df)

    st.bar_chart(df["category"].value_counts())
    st.area_chart(df["status"].value_counts())

    # api integration
    st.markdown("### 🤖 Ask AI About Cyber Incidents")
    user_q = st.text_input("Ask about CVEs, SIEM alerts, logs, threats:")
    if st.button("Ask Cyber AI"):
        if user_q.strip():
            answer = ai.query_database("cybersecurity", incident_manager.get_all_incidents, user_q,10)
            st.write(answer)

    # --- Permissions ---
    role = st.session_state.get("role", "")

    if role != "admin":
        st.warning("You do not have permission to perform CRUD on Cyber Incidents.")
        return

    #-----------------------------------CRUD---------------------------------------------

    st.subheader("⚠️ Add New Incident")
    with st.form("add_incident_form"):
        description = st.text_input("Incident Description")
        category = st.text_input("Category")
        status = st.selectbox("Status", ["Open", "In Progress", "Closed"])
        severity = st.selectbox("Severity", ["Critical", "High", "Medium", "Low"])
        submit = st.form_submit_button("Add Incident")
        if submit:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            reported_by = st.session_state.get("username")
            incident_manager.insert_incident(timestamp, category, severity, status, description, reported_by)
            st.success("Incident added!")

    st.subheader("⚠️ Update Incident")
    with st.form("update_incident_form"):
        ID = st.number_input("Incident ID", min_value=1, step=1)
        new_status = st.selectbox("New Status", ["Open", "In Progress", "Closed"])
        submit = st.form_submit_button("Update")
        if submit:
            incident_manager.update_incident_status(ID, new_status)
            st.success("Incident updated!")

    st.subheader("⚠️ Delete Incident")
    with st.form("delete_incident_form"):
        del_id = st.number_input("ID to Delete", min_value=1, step=1)
        submit = st.form_submit_button("Delete")
        if submit:
            incident_manager.delete_incident(del_id)
            st.success("Incident deleted!")

if "login" not in st.session_state or not st.session_state.login:
    st.warning("⚠ Please log in to access this page.")
    st.stop()
else:
    cybersecurity_page()
    st.sidebar.subheader("Dashboard Navigation")
    st.sidebar.title("👤 Your Profile")

    st.sidebar.markdown(f"User: {st.session_state.username}")
    st.sidebar.markdown(f"Role: {st.session_state.role.title()}")

    if st.sidebar.button("Logout"):
        st.session_state.login = False
        st.session_state.username = ''
        st.session_state.role = ''
        st.rerun()