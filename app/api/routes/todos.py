from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.models import TodoCreate, TodoRead, TodoUpdate
from app.db.repository import (
    create_todo,
    get_todos,
    get_todo,
    update_todo,
    delete_todo
)

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
async def create_todo_endpoint(
    todo_create: TodoCreate,
    session: AsyncSession = Depends(get_db)
):
    """Tạo todo mới"""
    return await create_todo(session, todo_create)

@router.get("", response_model=list[TodoRead])
async def list_todos(session: AsyncSession = Depends(get_db)):
    """Lấy tất cả todos"""
    return await get_todos(session)

@router.get("/{todo_id}", response_model=TodoRead)
async def get_todo_endpoint(
    todo_id: int,
    session: AsyncSession = Depends(get_db)
):
    """Lấy 1 todo theo id"""
    db_todo = await get_todo(session, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.patch("/{todo_id}", response_model=TodoRead)
async def update_todo_endpoint(
    todo_id: int,
    update_data: TodoUpdate,
    session: AsyncSession = Depends(get_db)
):
    """Cập nhật todo (toggle completed hoặc fields khác)"""
    db_todo = await update_todo(
        session, todo_id, update_data.model_dump(exclude_unset=True)
    )
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_endpoint(
    todo_id: int,
    session: AsyncSession = Depends(get_db)
):
    """Xóa todo"""
    success = await delete_todo(session, todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return None