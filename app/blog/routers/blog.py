from fastapi import APIRouter, status, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List
import blog.schemas as schemas
from blog.database import get_db
from blog.models import Blog as blog_model
from blog.auth import get_current_user

router = APIRouter()

# POST --> Create record
@router.post('/', status_code=status.HTTP_201_CREATED, tags=['Blogs'])
def blog_create(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    new_blog = blog_model(title=request.title, body=request.body, user_id=current_user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# GET --> fetch records
@router.get('/', response_model=List[schemas.ShowBlogModel], tags=['Blogs']) # use List in response model because need to output in list of dict
def get_all_blogs(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    blogs = db.query(blog_model).filter(blog_model.user_id == current_user.id).all()
    return blogs

@router.get('/{id}', status_code=200, response_model=schemas.ShowBlogModel, tags=['Blogs'])
def get_blog_by_id(id, response: Response, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    # blog = db.query(models.Blog).get({"id": id})
    blog = db.query(blog_model).filter(blog_model.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f"Blog with {id} this ID is not available!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {id} this ID is not available!")
    return blog

# DELETE --> delete record
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blogs'])
def delete_blog(id, db:Session=Depends(get_db)):
    blog = db.query(blog_model).filter(blog_model.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {id} this ID is not available!")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"data": f"ID {id} blog is deleted."}

# PUT --> update record
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['Blogs'])
def update(request: schemas.Blog, id, db: Session = Depends(get_db)):
    blog = db.query(blog_model).filter(blog_model.id == id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {id} this ID is not available!")
    blog.update({blog_model.title: request.title, blog_model.body: request.body})
    db.commit()
    return "Updated"