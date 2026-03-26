# posto/utils/drive.py
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
import streamlit as st

# Escopos que você precisa para acessar o Google Drive
SCOPES = ["https://www.googleapis.com/auth/drive"]

def _get_service():
    """
    Cria o serviço do Google Drive usando credenciais do st.secrets.
    """
    # Converte o JSON do secrets para dicionário
    creds_info = json.loads(st.secrets["gdrive"]["credentials"])
    
    # Cria credenciais de serviço
    creds = service_account.Credentials.from_service_account_info(
        creds_info,
        scopes=SCOPES
    )
    
    # Cria o serviço do Drive
    service = build("drive", "v3", credentials=creds)
    return service

def list_files(folder_id=None):
    """
    Lista arquivos na pasta do Google Drive.
    Se folder_id for None, lista todos os arquivos do Drive.
    """
    service = _get_service()
    query = f"'{folder_id}' in parents" if folder_id else None

    results = service.files().list(
        q=query,
        pageSize=100,
        fields="files(id, name, mimeType)"
    ).execute()
    
    files = results.get("files", [])
    return files

def upload_file(file_path, folder_id=None):
    """
    Faz upload de um arquivo para o Google Drive.
    """
    from googleapiclient.http import MediaFileUpload

    service = _get_service()
    file_metadata = {"name": file_path.split("/")[-1]}
    if folder_id:
        file_metadata["parents"] = [folder_id]

    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()
    return file