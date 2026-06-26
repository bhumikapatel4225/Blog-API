from fastapi import APIRouter, Depends, HTTPException, status
import blog.models as models
from blog.database import get_db
from sqlalchemy.orm import Session
from blog.hashing import Hash
from blog.auth import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post('/')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials!", headers={"WWW-Authenticate": "Bearer"})
    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Password!")
    # Generate JWT token
    access_token = create_access_token(data={'id': user.id, 'email': user.email})
    return {"access_token": access_token, "token_type": "bearer"}