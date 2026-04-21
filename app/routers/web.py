from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import CATEGORY_CODES, CATEGORY_LABELS
from app.dependencies import get_db_session
from app.services.computer_service import get_active_computers_by_category, get_computer_by_id

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"categories": CATEGORY_LABELS, "title": "Choose a PC for your task"},
    )


@router.get("/catalog", response_class=HTMLResponse)
def catalog(
    request: Request,
    category: str = Query(...),
    db: Session = Depends(get_db_session),
):
    if category not in CATEGORY_CODES:
        raise HTTPException(status_code=400, detail="Invalid category")
    computers = get_active_computers_by_category(db, category)
    return templates.TemplateResponse(
        request,
        "catalog.html",
        {
            "category": category,
            "category_label": CATEGORY_LABELS.get(category, category),
            "categories": CATEGORY_LABELS,
            "computers": computers,
        },
    )


@router.get("/computers/{computer_id}", response_class=HTMLResponse)
def computer_detail(request: Request, computer_id: int, db: Session = Depends(get_db_session)):
    computer = get_computer_by_id(db, computer_id)
    if not computer or not computer.is_active:
        raise HTTPException(status_code=404, detail="Computer not found")

    return templates.TemplateResponse(
        request,
        "computer_detail.html",
        {"computer": computer, "categories": CATEGORY_LABELS},
    )
