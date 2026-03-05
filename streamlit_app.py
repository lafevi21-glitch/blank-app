import streamlit as app

# 1. SET PAGE CONFIG (Must be the very first Streamlit command)
app.set_page_config(page_title="Login", initial_sidebar_state="collapsed")

# 2. HIDE SIDEBAR WITH CSS
app.markdown(
    """
    <style>
        /* Hides the sidebar entirely */
        [data-testid="stSidebar"] {
            display: none;
        }
        /* Hides the small arrow button that opens the sidebar */
        [data-testid="stSidebarCollapsedControl"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

matt = {"username": "Mateo", "password": "210812"}

def authenticate():
    app.header("Authenticate.")
    app.write("Please enter the password and agree to the terms and conditions to be able to proceed")

    na_username = app.text_input("Enter username")
    na_password = app.text_input("Enter password", type="password")

    if app.button("Login"):
        if na_username == matt["username"] and na_password == matt["password"]:
            # Store data in session state for the next page
            app.session_state["logged_user"] = na_username
            # Switch to the page inside the 'pages' folder
            app.switch_page("pages/multiapps.py") 
        else:
            app.error("Invalid username or password")

authenticate()