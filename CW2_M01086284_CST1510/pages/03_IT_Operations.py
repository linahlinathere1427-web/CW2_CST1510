#------------------------------------REQUIRED CONNECTIONS----------------------------------

import streamlit as st
import pandas as pd
from datetime import datetime

from app.data.tickets import ITTicketManager
from gemini_basic import AIQueryManager

ticket_manager=ITTicketManager()
ai=AIQueryManager()

#--------------------------------IT OPERATIONS DASHBOARD----------------------------------

def itops_page():
    st.title("🖥️ IT Operations Dashboard")

    df = ticket_manager.get_all_tickets()
    st.subheader("🗄️ Tickets Table")
    st.dataframe(df)

    st.bar_chart(df["priority"].value_counts())
    st.area_chart(df["status"].value_counts())

    # ---- AI Section ----
    st.markdown("🤖  Ask AI About IT Operations")
    user_q = st.text_input("Ask about RCA, performance issues, bottlenecks:")
    if st.button("Ask IT AI"):
        if user_q.strip():
            answer = ai.query_database("itops", ticket_manager.get_all_tickets, user_q)
            st.write(answer)

    role = st.session_state.get("role", "")

    if role not in ["admin", "analyst"]:
        st.warning("You cannot perform CRUD on IT tickets.")
        return

    #-----------------------------------CRUD-------------------------------------------

    st.subheader("⚠️ Add New Ticket")
    with st.form("add_ticket_form"):
        desc = st.text_input("Description")
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        status = st.selectbox("Status", ["Resolved", "Open", "In Progress", "Waiting for User"])
        assigned_to = st.selectbox("Assigned To", ["IT_Support_A", "IT_Support_B", "IT_Support_C"])
        resolution_hours = st.number_input("Resolution Time (hours)", min_value=0)
        submit = st.form_submit_button("Add")
        if submit:
            created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ticket_manager.insert_ticket(priority, desc, status, assigned_to, created, resolution_hours)
            st.success("Ticket added!")

    st.subheader("⚠️ Update Ticket")
    with st.form("update_ticket_form"):
        ID = st.number_input("Ticket ID", min_value=1)
        new_status = st.selectbox("New Status", ["Resolved", "Open", "In Progress", "Waiting for User"])
        submit = st.form_submit_button("Update")
        if submit:
            ticket_manager.update_ticket_status(ID, new_status)
            st.success("Ticket updated!")

    st.subheader("⚠️ Delete Ticket")
    with st.form("delete_ticket_form"):
        ID = st.number_input("ID to Delete", min_value=1)
        submit = st.form_submit_button("Delete")
        if submit:
            ticket_manager.delete_ticket(ID)
            st.success("Ticket deleted!")

#---------------------making sure pages shows up only after login-------------------------

if "login" not in st.session_state or not st.session_state.login:
    st.warning("⚠ Please log in to access this page.")
    st.stop()
else:
    itops_page()
    st.sidebar.subheader("Dashboard Navigation")
    st.sidebar.title("👤 Your Profile")

    st.sidebar.markdown(f"User: {st.session_state.username}")
    st.sidebar.markdown(f"Role: {st.session_state.role.title()}")

    if st.sidebar.button("Logout"):
        st.session_state.login = False
        st.session_state.username = ''
        st.session_state.role = ''
        st.rerun()