# utils/drive.py
import streamlit as st

def list_files(folder_id: str):
    """Exemplo: retorna lista simulada de arquivos"""
    # Aqui você pode implementar a lógica real usando Google Drive API
    return [
        {"name": "arquivo1.pdf", "size": 2*1024*1024, "mimeType": "application/pdf", "data": b""},
        {"name": "arquivo2.xlsx", "size": 5*1024*1024, "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "data": b""},
        {"name": "arquivo3.txt", "size": 1024, "mimeType": "text/plain", "data": b""},
    ]