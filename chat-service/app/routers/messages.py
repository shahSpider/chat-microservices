from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, database

router = APIRouter()

@router.get("/rooms/{room_id}/messages")
def get_messages(room_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Message).filter(models.Message.room_id == room_id).all()
