from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import CATEGORY_CODES, CATEGORY_LABELS, settings
from app.dependencies import get_db_session, require_admin
from app.models import Computer
from app.schemas import AdminComputerForm
from app.services.admin_service import create_computer, delete_computer, list_all_computers, update_computer

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="app/templates")


def _redirect(url: str) -> RedirectResponse:
    return RedirectResponse(url=url, status_code=303)


@router.get("/login", response_class=HTMLResponse)
def admin_login_page(request: Request):
    return templates.TemplateResponse(request, "admin_login.html", {"error": None})


@router.post("/login")
def admin_login(request: Request, password: str = Form(...)):
    if password != settings.admin_password:
        return templates.TemplateResponse(request, "admin_login.html", {"error": "Неверный пароль"}, status_code=401)

    request.session["is_admin"] = True
    return _redirect("/admin/computers")


@router.post("/logout")
def admin_logout(request: Request):
    request.session.clear()
    return _redirect("/admin/login")


@router.get("/computers", response_class=HTMLResponse, dependencies=[Depends(require_admin)])
def admin_computers(request: Request, db: Session = Depends(get_db_session)):
    computers = list_all_computers(db)
    return templates.TemplateResponse(
        request,
        "admin_computers.html",
        {"computers": computers, "categories": CATEGORY_LABELS},
    )


@router.get("/computers/new", response_class=HTMLResponse, dependencies=[Depends(require_admin)])
def admin_new_form(request: Request):
    return templates.TemplateResponse(
        request,
        "admin_computer_form.html",
        {"computer": None, "categories": CATEGORY_CODES, "action": "new"},
    )


@router.post("/computers/new", dependencies=[Depends(require_admin)])
def admin_create(
    db: Session = Depends(get_db_session),
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    cpu: str = Form(...),
    gpu: str = Form(""),
    ram_gb: int = Form(...),
    ssd_gb: int = Form(...),
    has_windows: bool = Form(False),
    image_url: str = Form(...),
    shop_name: str = Form(...),
    shop_url: str = Form(...),
    category_code: str = Form(...),
    is_active: bool = Form(False),
):
    if category_code not in CATEGORY_CODES:
        raise HTTPException(status_code=400, detail="Неверная категория")
    form = AdminComputerForm(
        name=name,
        description=description,
        price=price,
        cpu=cpu,
        gpu=gpu or None,
        ram_gb=ram_gb,
        ssd_gb=ssd_gb,
        has_windows=has_windows,
        image_url=image_url,
        shop_name=shop_name,
        shop_url=shop_url,
        category_code=category_code,
        is_active=is_active,
    )
    create_computer(db, form)
    return _redirect("/admin/computers")


@router.get("/computers/{computer_id}/edit", response_class=HTMLResponse, dependencies=[Depends(require_admin)])
def admin_edit_form(request: Request, computer_id: int, db: Session = Depends(get_db_session)):
    computer = db.get(Computer, computer_id)
    if not computer:
        raise HTTPException(status_code=404, detail="Не найдено")
    return templates.TemplateResponse(
        request,
        "admin_computer_form.html",
        {"computer": computer, "categories": CATEGORY_CODES, "action": "edit"},
    )


@router.post("/computers/{computer_id}/edit", dependencies=[Depends(require_admin)])
def admin_edit(
    computer_id: int,
    db: Session = Depends(get_db_session),
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    cpu: str = Form(...),
    gpu: str = Form(""),
    ram_gb: int = Form(...),
    ssd_gb: int = Form(...),
    has_windows: bool = Form(False),
    image_url: str = Form(...),
    shop_name: str = Form(...),
    shop_url: str = Form(...),
    category_code: str = Form(...),
    is_active: bool = Form(False),
):
    computer = db.get(Computer, computer_id)
    if not computer:
        raise HTTPException(status_code=404, detail="Не найдено")
    if category_code not in CATEGORY_CODES:
        raise HTTPException(status_code=400, detail="Неверная категория")

    form = AdminComputerForm(
        name=name,
        description=description,
        price=price,
        cpu=cpu,
        gpu=gpu or None,
        ram_gb=ram_gb,
        ssd_gb=ssd_gb,
        has_windows=has_windows,
        image_url=image_url,
        shop_name=shop_name,
        shop_url=shop_url,
        category_code=category_code,
        is_active=is_active,
    )
    update_computer(db, computer, form)
    return _redirect("/admin/computers")


@router.post("/computers/{computer_id}/delete", dependencies=[Depends(require_admin)])
def admin_delete(computer_id: int, db: Session = Depends(get_db_session)):
    computer = db.get(Computer, computer_id)
    if not computer:
        raise HTTPException(status_code=404, detail="Не найдено")
    delete_computer(db, computer)
    return _redirect("/admin/computers")
