# main.py
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
    token = request.cookies.get("session_token")
    return token is not None and token in sessions


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    if sessao_valida(request):
        return RedirectResponse("/files")
    return RedirectResponse("/login")


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if sessao_valida(request):
        return RedirectResponse("/files")
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(request: Request, usuario: str = Form(...), senha: str = Form(...)):
    if autenticar(usuario, senha):
        token = criar_sessao()
        sessions[token] = usuario
        response = RedirectResponse("/files", status_code=303)
        response.set_cookie("session_token", token, httponly=True)
        return response
    return templates.TemplateResponse("login.html", {
        "request": request,
        "erro": "Usuário ou senha inválidos"
    })


@app.get("/logout")
async def logout(request: Request):
    token = request.cookies.get("session_token")
    sessions.pop(token, None)
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("session_token")
    return response


@app.get("/files", response_class=HTMLResponse)
async def files_page(request: Request):
    if not sessao_valida(request):
        return RedirectResponse("/login")
    return templates.TemplateResponse("files.html", {"request": request})


@app.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request):
    if not sessao_valida(request):
        return RedirectResponse("/login")
    return templates.TemplateResponse("reports.html", {"request": request})


@app.get("/docs", response_class=HTMLResponse)
async def docs_page(request: Request):
    if not sessao_valida(request):
        return RedirectResponse("/login")
    return templates.TemplateResponse("docs.html", {"request": request})
