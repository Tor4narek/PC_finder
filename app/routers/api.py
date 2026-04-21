from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.config import CATEGORY_CODES
from app.dependencies import get_db_session
from app.schemas import ClassifyRequest, ClassifyResponse, ComputerOut
from app.services.classifier import classify_query
from app.services.computer_service import get_active_computers_by_category

router = APIRouter(prefix="/api", tags=["api"])


@router.post("/classify", response_model=ClassifyResponse)
async def classify(payload: ClassifyRequest):
    result = await classify_query(payload.query)
    return ClassifyResponse(**result)


@router.get("/computers", response_model=list[ComputerOut])
def list_computers(
    category: str = Query(...),
    db: Session = Depends(get_db_session),
):
    if category not in CATEGORY_CODES:
        raise HTTPException(status_code=400, detail="Invalid category")
    return get_active_computers_by_category(db, category)
