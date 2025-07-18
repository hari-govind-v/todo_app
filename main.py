from fastapi import Depends, FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from models.Models import *
from constants.testdata import data_list
from contextlib import asynccontextmanager
from db_connector.database import *
from sqlalchemy.orm import Session
from db_connector.dependencies import get_db
from db_connector.models import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def home_page():
    return JSONResponse(content={"message": "welcome to home page"}, status_code=status.HTTP_200_OK)

@app.post("/tasks")
async def create_task(task:TaskCreate, db: Session = Depends(get_db)):
    existing_task = db.query(Task).filter(Task.id == task.id).first()
    if existing_task:
        raise HTTPException(status_code=400, detail="Item already exists")
    
    new_task = Task(
        id=task.id,
        name=task.name,
        description=task.description,
        status=task.status 
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@app.get("/tasks", response_model=list[TaskCreate]) 
async def get_all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task: 
        raise HTTPException(status_code=404, detail="Item not found") 
    return task

@app.put("/tasks/{task_id}")
async def update_task_by_id(task_id: int, task: TaskBase, db: Session = Depends(get_db)):
    existing_task = db.query(Task).filter(Task.id == task_id).first()
    if not existing_task:
        raise HTTPException(status_code=400, detail="Item does not exist")
    existing_task.name = task.name
    existing_task.description = task.description
    existing_task.status = task.status

    db.commit()
    db.refresh(existing_task) 
    return existing_task

@app.delete("/tasks/{task_id}")
async def delete_task_by_id(task_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    task_to_be_deleted = db.query(Task).filter(Task.id == task_id).first()
    if not task_to_be_deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task_to_be_deleted)
    db.commit()

    return {"message": f"Task with id {task_id} deleted successfully"}

@app.patch("/tasks/{task_id}/update_status")
async def update_task_status(task_id: int, task_status : TaskStatus, db: Session = Depends(get_db)): 
    existing_task = db.query(Task).filter(Task.id == task_id).first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    existing_task.status = task_status.status
    db.commit()
    db.refresh(existing_task)

    return existing_task