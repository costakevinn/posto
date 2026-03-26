# routers/auth.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from utils.auth import autenticar
from utils.session import criar_sessao, sessao_valida, remover_sessao

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_token(request: Request) -> str | None:
    return request.query_params.get("token") or request.cookies.get("session_token")


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    token = get_token(request)
    if sessao_valida(token):
        return RedirectResponse(f"/files?token={token}")
    return RedirectResponse("/login")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    token = get_token(request)
    if sessao_valida(token):
        return RedirectResponse(f"/files?token={token}")
    return templates.TemplateResponse(request, "login.html")


@router.post("/login")
async def login(request: Request, usuario: str = Form(...), senha: str = Form(...)):
    if autenticar(usuario, senha):
        token = criar_sessao(usuario)
        return RedirectResponse(f"/files?token={token}", status_code=303)
    return templates.TemplateResponse(request, "login.html", {
        "erro": "Usuário ou senha inválidos"
    })


@router.get("/logout")
async def logout(request: Request):
    remover_sessao(get_token(request))
    return RedirectResponse("/login", status_code=303)
