# posto/utils/drive.py
import json
import streamlit as st
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/drive"]

def _get_service():
    """
    Cria o serviço do Google Drive usando credenciais do st.secrets.
    """
    creds_info = json.loads(st.secrets["gdrive"]["credentials"])
    creds = service_account.Credentials.from_service_account_info(
        creds_info,
        scopes=SCOPES
    )
    service = build("drive", "v3", credentials=creds)
    return service

def list_files(folder_id=None):
    """
    Lista arquivos na pasta do Drive.
    Para teste sem Drive, retorna stub.
    """
    # --- STUB para testes sem Drive ---
    if st.secrets.get("use_stub", True):
        return [
            {"id": "1", "name": "teste.txt", "mimeType": "text/plain", "size": 1024, "data": b"Hello World"}
        ]
    
    # --- Produção ---
    service = _get_service()
    query = f"'{folder_id}' in parents" if folder_id else None
    results = service.files().list(
        q=query,
        pageSize=100,
        fields="files(id, name, mimeType, size)"
    ).execute()
    files = results.get("files", [])
    for f in files:
        f["data"] = None  # Placeholder para download
    return files

def upload_file(file_path, folder_id=None):
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