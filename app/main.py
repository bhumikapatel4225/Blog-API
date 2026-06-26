from fastapi import FastAPI
import blog.models as models
from blog.database import engine
from blog.routers import blog, user, authentication

app = FastAPI()

app.include_router(authentication.router, prefix="/login", tags=["Auth"])
app.include_router(blog.router, prefix="/blog", tags=["Blogs"])
app.include_router(user.router, prefix="/user", tags=["Users"])

# create all the tables while run code
models.Base.metadata.create_all(engine)
