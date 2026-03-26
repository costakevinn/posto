# utils/gdrive.py
import os
import json
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

GDRIVE_FOLDER_ID = "1io5X9pUbWtleUIhE4B_Ks8c8dDLuxZpY"
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def _credenciais():
    info = {
        "type": os.environ["GDRIVE_TYPE"],
        "project_id": os.environ["GDRIVE_PROJECT_ID"],
        "private_key_id": os.environ["GDRIVE_PRIVATE_KEY_ID"],
        "private_key": os.environ["GDRIVE_PRIVATE_KEY"].replace("\\n", "\n"),
        "client_email": os.environ["GDRIVE_CLIENT_EMAIL"],
        "client_id": os.environ["GDRIVE_CLIENT_ID"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
    return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)


def listar_arquivos() -> list[dict]:
    """Lista todos os arquivos da pasta do Drive recursivamente."""
    creds = _credenciais()
    service = build("drive", "v3", credentials=creds)
    arquivos = []
    _coletar(service, GDRIVE_FOLDER_ID, "", arquivos)
    return arquivos


def _coletar(service, folder_id: str, caminho: str, resultado: list):
    page_token = None
    while True:
        resp = service.files().list(
            q=f"'{folder_id}' in parents and trashed = false",
            fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)",
            pageSize=1000,
            pageToken=page_token,
        ).execute()

        for item in resp.get("files", []):
            item["_caminho"] = f"{caminho}/{item['name']}" if caminho else item["name"]
            if item["mimeType"] == "application/vnd.google-apps.folder":
                _coletar(service, item["id"], item["_caminho"], resultado)
            else:
                resultado.append(item)

        page_token = resp.get("nextPageToken")
        if not page_token:
            break


def baixar_arquivo(file_id: str) -> tuple[bytes, str]:
    """Baixa um arquivo pelo ID. Retorna (conteudo, nome)."""
    creds = _credenciais()
    service = build("drive", "v3", credentials=creds)

    meta = service.files().get(fileId=file_id, fields="name, mimeType").execute()
    nome = meta["name"]

    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, service.files().get_media(fileId=file_id))
    done = False
    while not done:
        _, done = downloader.next_chunk()

    return buffer.getvalue(), nome
