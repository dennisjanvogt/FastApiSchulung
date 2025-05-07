from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate


class CRUDBook(CRUDBase[Book, BookCreate, BookUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: BookCreate, owner_id: int
    ) -> Book:
        obj_in_data = obj_in.dict()
        db_obj = Book(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Book]:
        return (
            db.query(self.model)
            .filter(Book.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
    def get_by_isbn(self, db: Session, *, isbn: str) -> Optional[Book]:
        return db.query(Book).filter(Book.isbn == isbn).first()


book = CRUDBook(Book)