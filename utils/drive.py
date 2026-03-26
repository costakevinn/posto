import io
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def _get_service():
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["gdrive"]["credentials"],
        scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)

def list_files() -> list[dict]:
    folder_id = st.secrets["gdrive"]["folder_id"]
    service = _get_service()
    query = f"'{folder_id}' in parents and trashed = false"
    result = service.files().list(
        q=query,
        fields="files(id, name, mimeType, size, modifiedTime)",
        orderBy="name"
    ).execute()
    return result.get("files", [])

def download_file(file_id: str) -> bytes:
    service = _get_service()
    request = service.files().get_media(fileId=file_id)
    buffer = io.BytesIO()
    MediaIoBaseDownload(buffer, request).next_chunk()
    return buffer.getvalue()