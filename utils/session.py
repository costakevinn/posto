# utils/session.py
import secrets

# Sessões ativas em memória
sessions: dict[str, str] = {}


def criar_sessao(usuario: str) -> str:
    token = secrets.token_hex(32)
    sessions[token] = usuario
    return token


def sessao_valida(token: str | None) -> bool:
    return token is not None and token in sessions


def remover_sessao(token: str | None):
    if token:
        sessions.pop(token, None)
