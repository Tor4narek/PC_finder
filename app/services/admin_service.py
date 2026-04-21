from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Computer
from app.schemas import AdminComputerForm


def list_all_computers(db: Session) -> list[Computer]:
    stmt = select(Computer).order_by(Computer.created_at.desc())
    return list(db.scalars(stmt).all())


def create_computer(db: Session, form: AdminComputerForm) -> Computer:
    computer = Computer(**form.model_dump())
    db.add(computer)
    db.commit()
    db.refresh(computer)
    return computer


def update_computer(db: Session, computer: Computer, form: AdminComputerForm) -> Computer:
    for key, value in form.model_dump().items():
        setattr(computer, key, value)
    db.commit()
    db.refresh(computer)
    return computer


def delete_computer(db: Session, computer: Computer):
    db.delete(computer)
    db.commit()
