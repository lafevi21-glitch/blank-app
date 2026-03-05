import streamlit as app

if not "logged_user" in app.session_state:
    app.error("Please, make sure you are logged!")
    app.switch_page("streamlit_app.py")
    app.stop()

app.set_page_config(initial_sidebar_state="collapsed")

app.markdown(
    """
    <style>
        /* This hides the sidebar itself */
        [data-testid="stSidebar"] {
            display: none;
        }
        /* This hides the ' > ' arrow button that lets users open it */
        [data-testid="stSidebarCollapsedControl"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

ver = "1"

redirected_user = app.session_state.get("logged_user", "Guest")

def multiapps_main(username):
    
    app.header("✨ Multiapps V" + ver)
    app.subheader("Welcome "+ username + ".")
    app.write("This website aimed to serve me, Mateo. You'll be able to find some quite useful apps such as a music player and a calculator")
    app.divider()
    
    # Music Player.

    app.subheader("Music Library 🎹") 
    app.write("Welcome my music library!")
    url = app.text_input("Input the URL of your music.")
    try:
        if app.button("Play"):
            app.audio(url, format="audio/mp3")
    except Exception:
        app.error("Invalid URL provided, **make sure it's MP3**.")

multiapps_main(redirected_user)