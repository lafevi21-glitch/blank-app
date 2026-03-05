import streamlit as app

matt = {"username": "Mateo", "password": "210812"}
ver = "1"

def authenticate():
    app.title("Authenticate.")
    app.write("Please enter the password and agree to the terms and conditions to be able to proceed to the app.")
    
    na_username = app.text_input("Enter username")
    na_password = app.text_input("Enter password", type="password")
    
    if na_username == matt["username"] and na_password == matt["password"]:
        multiapps_main(na_username)
        

def multiapps_main(username):
    app.header("Multiapps V" + ver)
    app.subheader("Welcome Mateo.")
    app.write("This website aimed to serve me, Mateo. You'll be able to find some quite useful apps such as a music player and a calculator")

authenticate()