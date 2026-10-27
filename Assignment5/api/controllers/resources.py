from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, Response, status
from ..models import models


def create(db: Session, resource):
    db_resource = models.Resource(
        item=resource.item,
        amount=resource.amount
    )
    try:
        db.add(db_resource)
        db.commit()
        db.refresh(db_resource)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(getattr(e, "orig", e)))
    return db_resource


def read_all(db: Session):
    return db.query(models.Resource).all()


def read_one(db: Session, resource_id):
    return db.query(models.Resource).filter(models.Resource.id == resource_id).first()


def update(db: Session, resource_id, resource):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id)
    update_data = resource.model_dump(exclude_unset=True)
    try:
        db_resource.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(getattr(e, "orig", e)))
    return db_resource.first()


def delete(db: Session, resource_id):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id)
    try:
        db_resource.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(getattr(e, "orig", e)))
    return Response(status_code=status.HTTP_204_NO_CONTENT)