import streamlit as app
import multiapps

multiapps = app.Page("multiapps.py")

matt = {"username": "Mateo", "password": "210812"}
ver = "1"

def authenticate():
    app.header("Authenticate.")
    app.write("Please enter the password and agree to the terms and conditions to be able to proceed to the app.")
    
    na_username = app.text_input("Enter username")
    na_password = app.text_input("Enter password", type="password")
    
    if app.button("Login"):
        if na_username == matt["username"] and na_password == matt["password"]:
            app.empty()
            multiapps.redirected_user = na_username
            app.navigation(multiapps)



authenticate()