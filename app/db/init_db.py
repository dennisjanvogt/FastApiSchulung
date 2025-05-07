from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine
from app.core.security import get_password_hash
from app.models.user import User
from app.config import settings


def init_db(db: Session) -> None:
    # Tabellen erstellen
    Base.metadata.create_all(bind=engine)
    
    # Überprüfen, ob bereits ein Superuser existiert
    user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
    if not user:
        # Ersten Superuser erstellen
        user_in = User(
            email=settings.FIRST_SUPERUSER,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
        )
        db.add(user_in)
        db.commit()