import streamlit as st
import pandas as pd
from datetime import datetime
from app.data.datasets import DatasetManager
from gemini_basic import AIQueryManager

ai = AIQueryManager()

dataset_manager = DatasetManager()

#------------------------------------DATASETS DASHBOARRD------------------------------------

def datasets_page():
    st.title("📊 Data Science Dashboard ")

    df = dataset_manager.get_all_datasets()
    st.subheader("🗂️ Dataset Table")
    st.dataframe(df)

    st.bar_chart(df["source"].value_counts())

    # ---- AI Section ----
    st.markdown("### 🤖 Ask AI About Datasets")
    user_q = st.text_input("Ask AI about anomalies, insights, ML models:")
    if st.button("Ask DS AI"):
        if user_q.strip():
            answer = ai.query_database("datascience", dataset_manager.get_all_datasets, user_q)
            st.write(answer)

    role = st.session_state.get("role", "")

    if role not in ["admin", "analyst"]:
        st.warning("You cannot perform CRUD on datasets.")
        return

    #-------------------------------------CRUD------------------------------------------

    st.subheader("⚠️ Add New Dataset")
    with st.form("add_dataset_form"):
        name = st.text_input("Dataset Name")
        category = st.text_input("Category")
        source = st.selectbox("Source", ["data_scientist", "cyber_admin", "it_admin"])
        last_updated = st.date_input("Last Updated", value=datetime.today()).strftime("%Y-%m-%d")
        record_count = st.number_input("Record Count", min_value=0)
        file_size_mb = st.number_input("File Size (MB)", min_value=0.0)
        created_at = st.date_input("Created At", value=datetime.today()).strftime("%Y-%m-%d")

        submit = st.form_submit_button("Add")
        if submit:
            dataset_manager.insert_dataset(name, category, source, last_updated, record_count, file_size_mb, created_at)
            st.success("Dataset added!")

    st.subheader("⚠️ Update Dataset")
    with st.form("update_dataset_form"):
        ID = st.number_input("Dataset ID", min_value=1, step=1)
        new_cat = st.text_input("New Category")
        submit = st.form_submit_button("Update")
        if submit:
            dataset_manager.update_dataset_category(ID, new_cat)
            st.success("Dataset updated!")

    st.subheader("⚠️ Delete Dataset")
    with st.form("delete_dataset_form"):
        ID = st.number_input("Dataset ID to Delete", min_value=1)
        submit = st.form_submit_button("Delete")
        if submit:
            dataset_manager.delete_dataset(ID)
            st.success("Dataset deleted!")

#-----------------------------------INITIALIZING-------------------------------

if "login" not in st.session_state or not st.session_state.login:
    st.warning("⚠ Please log in to access this page.")
    st.stop()
else:
    datasets_page()
    st.sidebar.subheader("Dashboard Navigation")
    st.sidebar.title("👤 Your Profile")

    st.sidebar.markdown(f"User: {st.session_state.username}")
    st.sidebar.markdown(f"Role: {st.session_state.role.title()}")

    if st.sidebar.button("Logout"):
        st.session_state.login = False
        st.session_state.username = ''
        st.session_state.role = ''
        st.rerun()