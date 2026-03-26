# routers/files.py
import io
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from utils.session import sessao_valida
from utils.gdrive import listar_arquivos, baixar_arquivo

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_token(request: Request) -> str | None:
    return request.query_params.get("token") or request.cookies.get("session_token")


@router.get("/files", response_class=HTMLResponse)
async def files_page(request: Request):
    token = get_token(request)
    if not sessao_valida(token):
        return RedirectResponse("/login")
    arquivos = listar_arquivos()
    return templates.TemplateResponse(request, "files.html", {
        "token": token,
        "arquivos": arquivos,
    })


@router.get("/download/{file_id}")
async def download(request: Request, file_id: str):
    token = get_token(request)
    if not sessao_valida(token):
        return RedirectResponse("/login")
    conteudo, nome = baixar_arquivo(file_id)
    return StreamingResponse(
        io.BytesIO(conteudo),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={nome}"}
    )
