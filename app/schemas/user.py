from typing import Optional, List

from pydantic import BaseModel, EmailStr, validator


# Gemeinsame Eigenschaften
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False


# Eigenschaften beim Erstellen
class UserCreate(UserBase):
    email: EmailStr
    password: str
    
    @validator('password')
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError('Passwort muss mindestens 8 Zeichen lang sein')
        return v


# Eigenschaften beim Aktualisieren
class UserUpdate(UserBase):
    password: Optional[str] = None
    
    @validator('password')
    def password_min_length(cls, v):
        if v is not None and len(v) < 8:
            raise ValueError('Passwort muss mindestens 8 Zeichen lang sein')
        return v


# Eigenschaften in DB
class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Zusätzliche Eigenschaften beim Lesen
class User(UserInDBBase):
    pass


# Zusätzliche Eigenschaften in DB
class UserInDB(UserInDBBase):
    hashed_password: str