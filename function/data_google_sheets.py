import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st 

def leer_Datos_google_sheets():
    ruta_json = st.secrets["GOOGLE_SHEETS"]
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(ruta_json, scope)
    client = gspread.authorize(creds)
    
    sheet = client.open("Datos portfolio").sheet1
    
    data = sheet.get_all_records()
    
    username = data[0]["username"]
    clave = str(data[0]["clave"])
    
    
    return username,clave
    


