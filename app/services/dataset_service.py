import pandas as pd
import os
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

def update_dataset_status(dataset_id: str, db: Session, new_status: str, row_count: int | None = None):
    # dataset = db.query(Dataset).filter(Dataset.dataset_id==dataset_id).first()
    dataset = db.execute(select(Dataset).where(Dataset.dataset_id==dataset_id)).scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
    dataset.status = new_status
    if row_count is not None:
        dataset.row_count = row_count
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset

def get_dataset_rows(dataset_id: str, db: Session, user_id: str, limit: int = 100, page: int = 1):
    if limit < 1 or page < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Limit and page must be positive integers")
    filename = db.execute(select(Dataset).where(Dataset.dataset_id == dataset_id)).scalar_one_or_none()
    if not filename:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
    if filename.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to view this dataset")
    offset = (page - 1) * limit
    # rows = db.query(DatasetRows).filter(DatasetRows.dataset_id==dataset_id).offset(offset).limit(limit).all()
    rows = db.execute(select(DatasetRows).where(DatasetRows.dataset_id==dataset_id).offset(offset).limit(limit)).scalars().all()
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset rows not found")
    return rows

def export_dataset(dataset_id: str, db: Session, user_id: str):
    os.makedirs("app/exports", exist_ok=True)
    file = db.execute(select(Dataset).where(Dataset.dataset_id == dataset_id)).scalar_one_or_none()
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")
    if file.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to export this dataset")
    file_name = f"app/exports/cleaned_{dataset_id}.csv"
    batch = 10000
    offset = 0
    first_batch = True
    while True:
        rows = db.execute(select(DatasetRows).where(DatasetRows.dataset_id==dataset_id).offset(offset).limit(batch)).scalars().all()
        if not rows:
            break
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
          # "remark": u.remark
        }
        for u in rows
        ]
        df = pd.DataFrame(data)
        df.to_csv(file_name, mode='w' if first_batch else 'a', header=first_batch, index=False)
        first_batch = False
        offset += batch
    return file_name