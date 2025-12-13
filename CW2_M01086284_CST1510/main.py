
#-------------------------------required connections---------------------------------

import streamlit as st
import pandas as pd
from app.data.db import DatabaseManager
from app.data.csvfile import CSVLoader
from app.services.user_service import UserService

#------------------------------------------------------------------------------------

loader = CSVLoader()
db = DatabaseManager()
user = UserService()

#-------------------------function to check if the table is empty--------------------

def table_is_empty(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    return count == 0

# ------------------------------Initialize session state--------------------------------

if "login" not in st.session_state:
    st.session_state.login = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""

# ---------------------------------Loading CSV safely-----------------------------------
# Use a fresh connection inside a 'with' block for each DB operation
with db.connect() as conn:
    if table_is_empty(conn, "cyber_incidents"):
        loader.load_csv_to_table(conn, r"C:\Users\PC\Documents\CW2_M01086284_CST1510\DATA\cyber_incidents.csv", "cyber_incidents")

    if table_is_empty(conn, "datasets_metadata"):
        loader.load_csv_to_table(conn, r"C:\Users\PC\Documents\CW2_M01086284_CST1510\DATA\datasets_metadata.csv", "datasets_metadata")

    if table_is_empty(conn, "it_tickets"):
        loader.load_csv_to_table(conn, r"C:\Users\PC\Documents\CW2_M01086284_CST1510\DATA\it_tickets.csv", "it_tickets")


#------------------------------------ MAIN FUNCTION-------------------------------------
def main():
    if not st.session_state.login:
        st.title("\nMULTI DOMAIN INTELLIGENCE PLATFORM")
        st.markdown("🔐***Login or Register to view dashboard***")

        tab_login, tab_register = st.tabs(["Login", "Register"])

        # -------------------------- Register Tab --------------------------
        with tab_register:
            st.subheader("REGISTER")
            username = st.text_input("Enter Username: ", key="login_user").strip()
            password = st.text_input("Enter Password: ", key="login_pass", type="password").strip()
            pass_confirm = st.text_input("Confirm Password: ", key="confirm_pass", type="password").strip()
            role = st.selectbox("Role", ["user", "admin", "analyst"], key="role_selection")

            if st.button("Register", key="register"):
                is_valid, error_msg = user.validate_username(username)
                if not is_valid:
                    st.error(f'Error: {error_msg}')
                else:
                    is_valid, error_msg = user.validate_password(password)
                    if not is_valid:
                        st.error(f'Error: {error_msg}')
                    elif pass_confirm != password:
                        st.error("Error: Passwords do not match")
                    else:
                        user.register(username, password, role)
                        st.success("User Registered!")

        # -------------------------- Login Tab --------------------------
        with tab_login:
            st.subheader("LOGIN")
            username = st.text_input("Enter Username: ", key="register_user").strip()
            password = st.text_input("Enter Password: ", key="register_pass", type="password").strip()

            if st.button("Login"):
                success, msg = user.login(username, password)
                if success:
                    st.session_state.login = True
                    st.session_state.username = username

                    # Safe DB query to get role
                    with db.connect() as conn:
                        role_df = pd.read_sql_query(
                            "SELECT role FROM users WHERE username=?", conn, params=(username,)
                        )
                        st.session_state.role = role_df.iloc[0]['role']

                    st.rerun()

                else:
                    st.error(msg)

    else:
        # ---------------------- Dashboard ----------------------

        st.header(f"WELCOME {st.session_state.username.upper()} TO MULTI DOMAIN INTELLIGENCE PLATFORM")
        st.subheader("Use the sidebar to navigate through pages")

        st.title("👤 Your Profile")

        #streamlit with css to make the output more prettier

        st.markdown("""
        <style>
        .big-box {
            border: 3px solid #0099ff;
            padding: 20px;
            border-radius: 12px;
            background-color: #000000;
            font-size: 24px;    
            font-weight: bold;
            line-height: 1.5;
            color: white;   
        }
        </style>
        """, unsafe_allow_html=True)

        username = st.session_state.username
        role = st.session_state.role.title()

        st.markdown(f"""
        <div class="big-box">
            <b>User:</b> {username}<br>
            <b>Role:</b> {role}
        </div>
        """, unsafe_allow_html=True)

        if st.sidebar.button("Logout"):
            st.session_state.login = False
            st.session_state.username = ''
            st.session_state.role = ''
            st.rerun()


# ----------------------------------------------
if __name__ == "__main__":
    main()
