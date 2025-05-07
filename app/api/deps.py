from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.core.auth import get_current_user, get_current_active_superuser
from app.models.user import User


def get_db() -> Generator:
    """
    Erzeugt eine Datenbankverbindung als Dependency Injection.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()