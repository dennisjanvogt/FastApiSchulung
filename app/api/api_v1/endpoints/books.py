from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.auth import get_current_user
from app.crud.crud_book import book as crud_book
from app.models.user import User
from app.schemas.book import Book, BookCreate, BookUpdate

router = APIRouter()


@router.get("/", response_model=List[Book])
def read_books(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Ruft alle Bücher ab.
    """
    if current_user.is_superuser:
        books = crud_book.get_multi(db, skip=skip, limit=limit)
    else:
        books = crud_book.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return books


# app/api/api_v1/endpoints/books.py (nur create_book aktualisieren)
@router.post("/", response_model=Book)
def create_book(
    *,
    db: Session = Depends(get_db),
    book_in: BookCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Erstellt ein neues Buch.
    """
    try:
        # Prüfen, ob ISBN bereits existiert
        if book_in.isbn:
            existing_book = crud_book.get_by_isbn(db=db, isbn=book_in.isbn)
            if existing_book:
                raise HTTPException(
                    status_code=400, 
                    detail="Ein Buch mit dieser ISBN existiert bereits"
                )
        
        # Buch erstellen
        book = crud_book.create_with_owner(db=db, obj_in=book_in, owner_id=current_user.id)
        return book
    except Exception as e:
        # Bessere Fehlerbehandlung
        raise HTTPException(
            status_code=500,
            detail=f"Fehler beim Erstellen des Buches: {str(e)}"
        )


@router.put("/{id}", response_model=Book)
def update_book(
    *,
    db: Session = Depends(get_db),
    id: int,
    book_in: BookUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Aktualisiert ein Buch.
    """
    book = crud_book.get(db=db, id=id)
    if not book:
        raise HTTPException(status_code=404, detail="Buch nicht gefunden")
    if not current_user.is_superuser and book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Keine Berechtigung")
    book = crud_book.update(db=db, db_obj=book, obj_in=book_in)
    return book


@router.get("/{id}", response_model=Book)
def read_book(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Ruft ein Buch nach ID ab.
    """
    book = crud_book.get(db=db, id=id)
    if not book:
        raise HTTPException(status_code=404, detail="Buch nicht gefunden")
    if not current_user.is_superuser and book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Keine Berechtigung")
    return book


@router.delete("/{id}", response_model=Book)
def delete_book(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Löscht ein Buch.
    """
    book = crud_book.get(db=db, id=id)
    if not book:
        raise HTTPException(status_code=404, detail="Buch nicht gefunden")
    if not current_user.is_superuser and book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Keine Berechtigung")
    book = crud_book.remove(db=db, id=id)
    return book


@router.get("/isbn/{isbn}", response_model=Book)
def read_book_by_isbn(
    isbn: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Ruft ein Buch nach ISBN ab.
    """
    book = crud_book.get_by_isbn(db=db, isbn=isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Buch nicht gefunden")
    if not current_user.is_superuser and book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Keine Berechtigung")
    return book
