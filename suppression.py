import requests
import os
import streamlit as st
import gspread 
import pandas as pd

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

authorized_user = {"refresh_token": st.secrets["refresh_token"], "token_uri": "https://oauth2.googleapis.com/token", "client_id": st.secrets["client_id"], "client_secret": st.secrets["client_secret"], "scopes": ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"], "expiry": "2022-11-09T18:33:12.530288Z"}
gc, authorized_user = gspread.oauth_from_dict(credentials, authorized_user)

def getPubs(sh, worksheet):
    pubList = worksheet.col_values(1)
    pubList.pop(0)
    os.write(1,  f"{pubList}\n".encode())
    return pubList

def xmlSuppress(pubName, listingId, frame):
    api = frame[frame['Pub Name'] == pubName].iloc[0]['Uri']
    os.write(1,  f"{api}\n".encode())
    # api = 'https://tpapi.aws.mapquest.com/tpapi/listings/suppress'
    xmlBody = f'''<suppress>
                <listingId>{listingId}</listingId>
                <suppress>true</suppress>
                </suppress>
            '''
    row = frame[frame['Pub Name'] == pubName]
    if not row.empty and 'Header1 Key' in frame.columns:
        key = row.iloc[0]['Header1 Key']
    else:
        key = None
    if not row.empty and 'Header1 Value' in frame.columns:
        value = row.iloc[0]['Header1 Value']
    else:
        value = None
    # key = frame.loc[pubName, 'Header1 Key']
    heads = {
                'Content-Type': 'application/xml',
                f'{key}': f'{value}'
            }
    request = requests.post(api, headers = heads, data = xmlBody)
    # os.write(1,  f"{key}\n".encode())
    os.write(1,  f"{request.status_code}\n".encode())
    os.write(1,  f"{request.text}\n".encode())
    return

def jsonSuppress(pubName, listingId, frame):

    return

def userSelect():
    googSheet = 'https://docs.google.com/spreadsheets/d/1q1QcCD_wXY2QMMphScptTlSFOnsWA-35072U510oWVk/edit?gid=0#gid=0' #prod doc
    sh = gc.open_by_url(googSheet)
    worksheet = sh.get_worksheet(0)
    listOfPubs = getPubs(sh, worksheet)
    with st.form("Form"):
        option = st.selectbox(
            "What publisher?",
            (listOfPubs),
            index=None,
            placeholder="Select a publihser",
        )
        suppressId = st.text_input("What ID should be suppressed?")
        # canonicalId = st.text_input("What is the canonical ID?")
        form_submitted = st.form_submit_button("Suppress")

        if form_submitted:
            st.write(f"Attempting to suppress {suppressId} on {option}")
            # if canonicalId:
            #     st.write(f"Canonical ID is {canonicalId}")
            dataframe = pd.DataFrame(worksheet.get_all_records())
            os.write(1,  f"{dataframe}\n".encode())
            if option == 'MapQuest':
                xmlSuppress(option, suppressId, dataframe)
            # else:
            #     jsonSuppress(option, suppressId, dataframe)
            


userSelect()