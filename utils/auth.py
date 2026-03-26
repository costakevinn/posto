# utils/auth.py
import os
import hashlib
import secrets

AUTH_USERNAME = os.environ.get("AUTH_USERNAME")
AUTH_SALT     = os.environ.get("AUTH_SALT")
AUTH_HASH     = os.environ.get("AUTH_HASH")


def autenticar(usuario: str, senha: str) -> bool:
    senha_hash = hashlib.sha256((senha + AUTH_SALT).encode()).hexdigest()
    return usuario == AUTH_USERNAME and senha_hash == AUTH_HASH


def criar_sessao() -> str:
    return secrets.token_hex(32)
