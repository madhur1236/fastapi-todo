import schemas,models,database
from sqlalchemy.orm import Session
from fastapi import  Depends, HTTPException

get_db = database.get_db

def create_todo(todo: schemas.ToDoCreate, db: Session= Depends(get_db)):
    db_todo = models.ToDo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todos(completed:bool | None = None,skip: int =0, limit: int = 10, db: Session = Depends(get_db)):
    query = db.query(models.ToDo)
    if completed is not None:
        query = query.filter(models.ToDo.completed == completed)
    return query.offset(skip).limit(limit).all()

def get_todo(todo_id:int,db: Session = Depends(get_db)):
    todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail=f"To-Do with this id {todo_id} not found")
    return todo

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

def delete_todo(todo_id:int,db: Session = Depends(get_db)):
    todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "ToDo deleted successfully"}

def mark_complete(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.ToDo).filter(models.ToDo.id == todo_id).first()
    if not todo:
        raise HTTPException(stauts_code=404, details="Todo not found")
    
    todo.completed = True
    db.commit()
    db.refresh(todo)
    return todo

