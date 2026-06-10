import pandas as pd
import os
os.makedirs("app\exports", exist_ok=True)
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.dataset import Dataset, DatasetRows

def create_dataset_record(filename: str, user_id: str, db:Session):
    new_dataset = Dataset(filename=filename, user_id=user_id)
    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)
    return new_dataset

def get_dataset_by_id(dataset_id: str, db: Session):
    # dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
    dataset = db.execute(select(Dataset).where(Dataset.dataset_id == dataset_id)).scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
    return dataset

def get_user_datasets(user_id: str, db: Session):
    # datasets = db.query(Dataset).filter(Dataset.user_id == user_id).all()
    datasets = db.execute(select(Dataset).where(Dataset.user_id == user_id)).scalars().all()
    if not datasets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No datasets found for this user")
    return datasets

def update_dataset_status(dataset_id: str, db: Session, new_status: str):
    # dataset = db.query(Dataset).filter(Dataset.dataset_id==dataset_id).first()
    dataset = db.execute(select(Dataset).where(Dataset.dataset_id==dataset_id)).scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
    dataset.status = new_status
    db.commit()
    db.refresh(dataset)
    return dataset

def get_dataset_rows(dataset_id: str, db: Session, user_id: str, limit: int = 100, page: int = 1):
    filename = db.execute(select(Dataset).where(Dataset.dataset_id == dataset_id)).scalar_one_or_none()
    if filename.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to view this dataset")
    offset = (page - 1) * limit
    # rows = db.query(DatasetRows).filter(DatasetRows.dataset_id==dataset_id).offset(offset).limit(limit).all()
    rows = db.execute(select(DatasetRows).where(DatasetRows.dataset_id==dataset_id).offset(offset).limit(limit)).scalars().all()
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset rows not found")
    return rows

def export_dataset(dataset_id: str, db: Session, user_id: str):
    # rows = db.query(DatasetRows).filter(DatasetRows.dataset_id == dataset_id).all()
    rows = db.execute(select(DatasetRows).where(DatasetRows.dataset_id==dataset_id)).scalars().all()
    # filename = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()
    filename = db.execute(select(Dataset).where(Dataset.dataset_id == dataset_id)).scalar_one_or_none()
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset rows not found") 
    if filename.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to export this dataset")
    data = [
    {
        "user_id_field": u.user_id_field,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "sex": u.sex,
        "email": u.email,
        "phone": u.phone,
        "date_of_birth": u.date_of_birth,
        "job_title": u.job_title
    }
    for u in rows
    ]
    
    df = pd.DataFrame(data)
    file_name = f"exports/cleaned_{filename.filename}"
    df.to_csv(file_name, index=False)
    return file_name
