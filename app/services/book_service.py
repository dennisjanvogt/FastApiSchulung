from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.crud_book import book as crud_book
from app.models.user import User
from app.schemas.book import BookCreate, BookUpdate, Book
from app.exceptions import BookNotFoundException, BookAlreadyExistsException, NotEnoughPermissionException


class BookService:
    @staticmethod
    def get_books(
        db: Session, current_user: User, skip: int = 0, limit: int = 100
    ) -> List[Book]:
        """Ruft Bücher für den aktuellen Benutzer ab."""
        if current_user.is_superuser:
            return crud_book.get_multi(db, skip=skip, limit=limit)
        else:
            return crud_book.get_multi_by_owner(
                db=db, owner_id=current_user.id, skip=skip, limit=limit
            )

    @staticmethod
    def create_book(db: Session, book_in: BookCreate, current_user: User) -> Book:
        """Erstellt ein neues Buch."""
        if book_in.isbn:
            db_book = crud_book.get_by_isbn(db=db, isbn=book_in.isbn)
            if db_book:
                raise BookAlreadyExistsException()
        
        return crud_book.create_with_owner(
            db=db, obj_in=book_in, owner_id=current_user.id
        )

    @staticmethod
    def update_book(
        db: Session, id: int, book_in: BookUpdate, current_user: User
    ) -> Book:
        """Aktualisiert ein Buch."""
        book = crud_book.get(db=db, id=id)
        if not book:
            raise BookNotFoundException()
        
        if not current_user.is_superuser and book.owner_id != current_user.id:
            raise NotEnoughPermissionException()
        
        return crud_book.update(db=db, db_obj=book, obj_in=book_in)

    @staticmethod
    def get_book(db: Session, id: int, current_user: User) -> Book:
        """Ruft ein Buch nach ID ab."""
        book = crud_book.get(db=db, id=id)
        if not book:
            raise BookNotFoundException()
        
        if not current_user.is_superuser and book.owner_id != current_user.id:
            raise NotEnoughPermissionException()
        
        return book

    @staticmethod
    def delete_book(db: Session, id: int, current_user: User) -> Book:
        """Löscht ein Buch."""
        book = crud_book.get(db=db, id=id)
        if not book:
            raise BookNotFoundException()
        
        if not current_user.is_superuser and book.owner_id != current_user.id:
            raise NotEnoughPermissionException()
        
        return crud_book.remove(db=db, id=id)


book_service = BookService()