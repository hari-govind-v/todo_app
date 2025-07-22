
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .schemas import TaskCreateDTO, TaskBaseDTO, TaskStatusDTO
from .models import UserTask
from todo_app.core.dependencies import get_db
from todo_app.auth.utils import get_current_user
from todo_app.users.models import User

task_router = APIRouter()

@task_router.post("/")
async def create_task(
    userid: int,
    task: TaskCreateDTO, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if userid != current_user.id:
        raise HTTPException(status_code=402, detail="Session user and current user doesnt match")
    existing_task = db.query(UserTask).filter(UserTask.id == task.id).first()
    if existing_task:
        raise HTTPException(status_code=400, detail="Item already exists")
    
    new_task = UserTask(
        id=task.id,
        name=task.name,
        description=task.description,
        status=task.status ,
        user_id=current_user.id
    )

    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    return new_task


@task_router.get("/", response_model=list[TaskCreateDTO])
async def get_all_tasks(
    userid: int,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if userid != current_user.id:
        raise HTTPException(status_code=402, detail="Session user and current user doesnt match")
    try:
        tasks = db.query(UserTask).filter(UserTask.user_id == current_user.id).all()
        return tasks
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to retrieve tasks")


@task_router.get("/{task_id}")
async def get_task_by_id(
    userid: int,
    task_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if userid != current_user.id:
        raise HTTPException(status_code=402, detail="Session user and current user doesnt match")
    task = db.query(UserTask).filter(
        UserTask.id == task_id, 
        UserTask.user_id == current_user.id
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Item not found")
    return task


@task_router.put("/{task_id}")
async def update_task_by_id(
    userid: int,
    task_id: int, 
    task: TaskBaseDTO, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if userid != current_user.id:
        raise HTTPException(status_code=402, detail="Session user and current user doesnt match")
    existing_task = db.query(UserTask).filter(
        UserTask.id == task_id, 
        UserTask.user_id == current_user.id
    ).first()
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


@task_router.delete("/{task_id}")
async def delete_task_by_id(
    userid: int,
    task_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if userid != current_user.id:
        raise HTTPException(status_code=402, detail="Session user and current user doesnt match")
    task_to_be_deleted = db.query(UserTask).filter(
        UserTask.id == task_id, 
        UserTask.user_id == current_user.id
    ).first()
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


@task_router.patch("/{task_id}/update_status")
async def update_task_status(
    userid: int,
    task_id: int, 
    task_status: TaskStatusDTO, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if userid != current_user.id:
        raise HTTPException(status_code=402, detail="Session user and current user doesnt match")
    existing_task = db.query(UserTask).filter(
        UserTask.id == task_id,
        UserTask.user_id == current_user.id
    ).first()
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
