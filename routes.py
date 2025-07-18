
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.models import TaskCreate, TaskBase, TaskStatus
from db_connector.models import Task
from db_connector.dependencies import get_db

router = APIRouter()

@router.get("/")
async def home_page():
    return JSONResponse(content={"message": "welcome to home page"}, status_code=status.HTTP_200_OK)


@router.post("/tasks")
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    existing_task = db.query(Task).filter(Task.id == task.id).first()
    if existing_task:
        raise HTTPException(status_code=400, detail="Item already exists")
    
    new_task = Task(
        id=task.id,
        name=task.name,
        description=task.description,
        status=task.status 
    )

    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    return new_task


@router.get("/tasks", response_model=list[TaskCreate])
async def get_all_tasks(db: Session = Depends(get_db)):
    try:
        tasks = db.query(Task).all()
        return tasks
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to retrieve tasks")


@router.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Item not found")
    return task


@router.put("/tasks/{task_id}")
async def update_task_by_id(task_id: int, task: TaskBase, db: Session = Depends(get_db)):
    existing_task = db.query(Task).filter(Task.id == task_id).first()
    if not existing_task:
        raise HTTPException(status_code=400, detail="Item does not exist")

    try:
        existing_task.name = task.name
        existing_task.description = task.description
        existing_task.status = task.status
        db.commit()
        db.refresh(existing_task)
        return existing_task
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update task")


@router.delete("/tasks/{task_id}")
async def delete_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task_to_be_deleted = db.query(Task).filter(Task.id == task_id).first()
    if not task_to_be_deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        db.delete(task_to_be_deleted)
        db.commit()
        return JSONResponse(
            content={"message": f"Task with id {task_id} deleted successfully"},
            status_code=status.HTTP_200_OK
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete task")


@router.patch("/tasks/{task_id}/update_status")
async def update_task_status(task_id: int, task_status: TaskStatus, db: Session = Depends(get_db)):
    existing_task = db.query(Task).filter(Task.id == task_id).first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        existing_task.status = task_status.status
        db.commit()
        db.refresh(existing_task)
        return existing_task
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update task status")
