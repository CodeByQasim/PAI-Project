from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.user import User

router = APIRouter()

@router.get("/me")
def get_profile(db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/me")
def update_profile(full_name: str = None, bio: str = None, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if full_name:
        user.full_name = full_name
    if bio:
        user.bio = bio
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user
