from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date
from sqlalchemy.orm import relationship

from app.db.session import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    author = Column(String(255), index=True)
    description = Column(Text)
    publication_date = Column(Date)
    isbn = Column(String(13), unique=True, index=True)
    
    # Fremdschlüssel zum Besitzer
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Beziehung zum Besitzer
    owner = relationship("User", back_populates="books")