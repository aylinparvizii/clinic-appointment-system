from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..database.base import Base


class Specialty(Base):
    __tablename__ = "specialties"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
        )
    
    code = Column(
        String(3), 
        unique=True, 
        nullable=False,
        index=True
        )
    
    title = Column(
        String(100), 
        nullable=False
        )

    doctors = relationship(
        "Doctor",
        back_populates="specialty"
    )