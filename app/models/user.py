from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
import uuid
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime
from app.models.dataset import Dataset

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__='users'
    id = Column(String(36), default=generate_uuid, primary_key=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    dataset = relationship('Dataset',back_populates='user')
    