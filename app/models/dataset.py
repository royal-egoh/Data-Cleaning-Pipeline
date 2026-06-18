from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
import uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime, date

def generate_uuid():
    return str(uuid.uuid4())

class Dataset(Base):
    __tablename__='datasets'
    dataset_id =  Column(String(36),primary_key=True, default=generate_uuid, index=True, nullable=False)
    filename = Column(String, nullable=False)
    status = Column(String, default='pending')
    row_count = Column(Integer)
    uploaded_at =  Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)

    
    user = relationship('User',back_populates='dataset')
    rows = relationship('DatasetRows', back_populates='dataset')
    
class DatasetRows(Base):
    __tablename__='datasetrows'
    row_id = Column(String(36), default=generate_uuid, primary_key=True, index=True, nullable=False)
    dataset_id =  Column(String(36), ForeignKey('datasets.dataset_id'), index=True, nullable=False)
    row_index = Column(Integer)
    
    user_id_field = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    sex = Column(String)
    email = Column(String)
    phone = Column(String)
    date_of_birth = Column(Date)
    job_title = Column(String)
    # remark = Column(String)
    
    
    dataset = relationship('Dataset', back_populates='rows')
    
    
    
    
