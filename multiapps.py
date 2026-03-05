import streamlit as app

ver = "1"

redirected_user = "None"

def multiapps_main(username):
    
    app.header("✨ Multiapps V" + ver)
    app.subheader("Welcome"+ username + ".")
    app.write("This website aimed to serve me, Mateo. You'll be able to find some quite useful apps such as a music player and a calculator")

multiapps_main(redirected_user)