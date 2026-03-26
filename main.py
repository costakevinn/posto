import secrets
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from utils.auth import autenticar, criar_sessao

app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")

sessions = {}

def sessao_valida(request: Request) -> bool:
    token = request.query_params.get("token") or request.cookies.get("session_token")
    return token is not None and token in sessions

def get_token(request: Request) -> str | None:
    return request.query_params.get("token") or request.cookies.get("session_token")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    if sessao_valida(request):
        token = get_token(request)
        return RedirectResponse(f"/files?token={token}")
    return RedirectResponse("/login")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if sessao_valida(request):
        token = get_token(request)
        return RedirectResponse(f"/files?token={token}")
    return templates.TemplateResponse(request, "login.html")

@app.post("/login")
async def login(request: Request, usuario: str = Form(...), senha: str = Form(...)):
    if autenticar(usuario, senha):
        token = criar_sessao()
        sessions[token] = usuario
        return RedirectResponse(f"/files?token={token}", status_code=303)
    return templates.TemplateResponse(request, "login.html", {"erro": "Usuário ou senha inválidos"})

@app.get("/logout")
async def logout(request: Request):
    token = get_token(request)
    sessions.pop(token, None)
    return RedirectResponse("/login", status_code=303)

@app.get("/files", response_class=HTMLResponse)
async def files_page(request: Request):
    if not sessao_valida(request):
        return RedirectResponse("/login")
    token = get_token(request)
    return templates.TemplateResponse(request, "files.html", {"token": token})

@app.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request):
    if not sessao_valida(request):
        return RedirectResponse("/login")
    token = get_token(request)
    return templates.TemplateResponse(request, "reports.html", {"token": token})

@app.get("/docs", response_class=HTMLResponse)
async def docs_page(request: Request):
    if not sessao_valida(request):
        return RedirectResponse("/login")
    token = get_token(request)
    return templates.TemplateResponse(request, "docs.html", {"token": token})
