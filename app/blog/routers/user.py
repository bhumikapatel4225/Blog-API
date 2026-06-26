from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from blog.hashing import Hash
import blog.schemas as schemas
from blog.models import User as user_model
from blog.database import get_db

router = APIRouter()

# Create User
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUsermodel, tags=['Users'])
def user_create(request: schemas.User, db: Session = Depends(get_db)):
    hashedPassword = Hash.bcrypt(request.password)
    new_user = user_model.User(name=request.name, email=request.email, password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', status_code=200, response_model=schemas.ShowUsermodel, tags=['Users'])
def get_user(id, db: Session = Depends(get_db)):
    users = db.query(user_model.User).filter(user_model.User.id == id).first()
    return users