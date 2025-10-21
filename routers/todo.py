from fastapi import APIRouter, status, Depends
import schemas, database
from repository import todo
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix='/todos',
    tags=['todo']
)

todos = []

get_db = database.get_db

@router.post('/', response_model=schemas.ToDo, status_code=status.HTTP_201_CREATED)
def create_todo(request: schemas.ToDoCreate, db: Session= Depends(get_db)):
    return todo.create_todo(request,db)

@router.get('/',response_model=List[schemas.ToDo],status_code=status.HTTP_200_OK)
def get_todos(completed:bool | None = None,skip: int =0, limit: int = 10, db: Session = Depends(get_db)):
    return todo.get_todos(completed,skip,limit,db)

@router.get('/{todo_id}',response_model=schemas.ToDo,status_code=status.HTTP_200_OK)
def get_todo(todo_id:int,db: Session = Depends(get_db)):
    return todo.get_todo(todo_id,db)

@router.put('/{todo_id}', response_model = schemas.ToDo)
def update_todo(todo_id: int, updated_todo: schemas.ToDoUpdate,db: Session = Depends(get_db)):
    return todo.update_todo(todo_id,updated_todo,db)

@router.delete("/{todo_id}")
def delete_todo(todo_id:int,db: Session = Depends(get_db)):
    return todo.delete_todo(todo_id,db)