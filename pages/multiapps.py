import streamlit as app
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

ver = "1"

app.set_page_config(page_title="MultiApps V" + ver, page_icon="✨")

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

redirected_user = app.session_state.get("logged_user", "Guest")

def multiapps_main(username):
    
    app.header("✨ Multiapps V" + ver)
    app.subheader("Welcome "+ username + ".")
    app.write("This website aimed to serve me, Mateo. You'll be able to find some quite useful apps such as a music player and a calculator")
    app.divider()
    
    # Music Player.

    app.subheader("Music Library 🎹") 
    app.write("Welcome to my music library!")
    url = app.text_input("Input the URL of your music.")
    try:
        if app.button("Play"):
            app.video(url, format="audio/mp3")
    except Exception:
        app.error("Invalid URL provided, **make sure it's MP3**.")
    
    # Music Player.

    app.divider()
    
    # Cloud Service.

    app.subheader("Cloud ☁")

    app.write("In this section you're able to upload files directly on Google Drive!")

    def get_drive_service():
        # This pulls directly from the secrets we just configured
        info = app.secrets["gcp_service_account"].to_dict()
        info["private_key"] = info["private_key"].replace("\\n", "\n")
        creds = service_account.Credentials.from_service_account_info(info)
        return build('drive', 'v3', credentials=creds)

    def upload_file(uploaded_file, folder_id):
        service = get_drive_service()
        file_metadata = {'name': uploaded_file.name, 'parents': [folder_id]}
        media = MediaIoBaseUpload(io.BytesIO(uploaded_file.getvalue()), 
                              mimetype=uploaded_file.type)
    
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return file.get('id')

    app.title("Secure Drive Upload")

    
    FOLDER_ID = "PASTE_YOUR_FOLDER_ID_HERE"

    myfile = app.file_uploader("Choose a file")
    if myfile and app.button("Upload to Drive"):
        fid = upload_file(myfile, FOLDER_ID)
        app.success(f"Uploaded! File ID: {fid}")

    app.divider()

    app.header("Hysterial AI 💻")
    app.write("Welcome to Mateo's personal AI assistant. Click the button below to start!")
    if app.button("Connect"):
        app.switch_page("pages/hysterialai_module.py")

    app.divider()

    app.header("Archive 📳")
    app.write("Welcome to my archive! Find all of my files here.")
    app.subheader("Documents 📄")

    # Documents

    app.Warning("Sorry, we're still in development!")

    # Documents





multiapps_main(redirected_user)
