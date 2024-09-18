import requests
import os
import streamlit as st

credentials = {
    "installed": {
        "client_id": st.secrets["client_id"],
        "project_id": st.secrets["project_id"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", 
        "client_secret": st.secrets["client_secret"],
        "redirect_uris":["http://localhost"]
    }    
}

os.write(1,  f"{credentials}\n".encode())