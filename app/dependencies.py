from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db


def get_db_session(db: Session = Depends(get_db)) -> Session:
    return db


def require_admin(request: Request):
    if not request.session.get("is_admin"):
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/admin/login"})
