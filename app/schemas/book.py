from typing import Optional
from datetime import date

from pydantic import BaseModel, validator, Field


# Gemeinsame Eigenschaften
class BookBase(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    publication_date: Optional[date] = None
    isbn: Optional[str] = None
    
    @validator('isbn')
    def isbn_valid(cls, v):
        if v is not None:
            if not v.isdigit():
                raise ValueError('ISBN muss nur aus Ziffern bestehen')
            if len(v) != 13 and len(v) != 10:
                raise ValueError('ISBN muss 10 oder 13 Zeichen lang sein')
        return v


# Eigenschaften beim Erstellen
class BookCreate(BookBase):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)


# Eigenschaften beim Aktualisieren
class BookUpdate(BookBase):
    pass


# Eigenschaften in DB
class BookInDBBase(BookBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# Zusätzliche Eigenschaften beim Lesen
class Book(BookInDBBase):
    pass


# Zusätzliche Eigenschaften in DB
class BookInDB(BookInDBBase):
    pass