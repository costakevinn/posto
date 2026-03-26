# routers/reports.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from utils.session import sessao_valida

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_token(request: Request) -> str | None:
    return request.query_params.get("token") or request.cookies.get("session_token")


@router.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request):
    token = get_token(request)
    if not sessao_valida(token):
        return RedirectResponse("/login")
    return templates.TemplateResponse(request, "reports.html", {"token": token})
