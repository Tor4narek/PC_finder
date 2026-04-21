from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Computer


def get_active_computers_by_category(db: Session, category: str) -> list[Computer]:
    stmt = (
        select(Computer)
        .where(Computer.is_active.is_(True), Computer.category_code == category)
        .order_by(Computer.price.asc())
    )
    return list(db.scalars(stmt).all())


def get_computer_by_id(db: Session, computer_id: int) -> Computer | None:
    return db.get(Computer, computer_id)
