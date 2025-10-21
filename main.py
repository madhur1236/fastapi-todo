from fastapi import FastAPI
import models
from database import engine
from sqlalchemy import or_
from routers import todo

app = FastAPI(title="To-Do App")
models.Base.metadata.create_all(engine)

app.include_router(todo.router)


# @app.get('/todos/search/',response_model = List[schemas.ToDo])
# def search_todos(q: str, db: Session = Depends(get_db)):
#     return db.query(models.ToDo).filter(
#         or_(
#             models.ToDo.title.ilike(f"%{q}%"),
#             models.ToDo.description.ilike(f"%{q}%")
#         )
#     ).all()

# @app.get("/todos/paginated")
# def get_paginated_todos(skip:int =0, limit: int = 10, db: Session = Depends(get_db)):
#     total = db.query(models.ToDo).count()
#     todos = db.query(models.ToDo).offset(skip).limit(limit).all()
#     return {"total": total, "skip": skip, "limit": limit,"data": todos}