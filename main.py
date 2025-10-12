from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends, status
from typing import List
import models, schemas,database
from database import engine
from sqlalchemy import or_

app = FastAPI(title="To-Do App")
models.Base.metadata.create_all(engine)

get_db = database.get_db
todos = []

# @app.get("/")
# def root():
#     return {"message": "Welcome to To-Do App"}

@app.post('/todos/', response_model=schemas.ToDo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDoCreate, db: Session= Depends(get_db)):
    db_todo = models.ToDo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.get('/todos/',response_model=List[schemas.ToDo],status_code=status.HTTP_200_OK)
def get_todos(completed:bool | None = None,skip: int =0, limit: int = 10, db: Session = Depends(get_db)):
    query = db.query(models.ToDo)
    if completed is not None:
        query = query.filter(models.ToDo.completed == completed)
    return query.offset(skip).limit(limit).all()

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

@app.get('/todos/{todo_id}',response_model=schemas.ToDo,status_code=status.HTTP_200_OK)
def get_todo(todo_id:int,db: Session = Depends(get_db)):
    todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail=f"To-Do with this id {todo_id} not found")
    return todo

@app.put('/todos/{todo_id}', response_model = schemas.ToDo)
def update_todo(todo_id: int, updated_todo: schemas.ToDoUpdate,db: Session = Depends(get_db)):
    todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail=f"To-Do with this id {todo_id} not found")
    
    update_data = updated_todo.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(todo,key,value)
    
    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int,db: Session = Depends(get_db)):
    todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "ToDo deleted successfully"}

@app.patch("/todos/{todo_id}/complete", response_model = schemas.ToDo)
def mark_complete(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if not todo:
        raise HTTPException(stauts_code=404, details="Todo not found")
    
    todo.completed = True
    db.commit()
    db.refresh(todo)
    return todo
