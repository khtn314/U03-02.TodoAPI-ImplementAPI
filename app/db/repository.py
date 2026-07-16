from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Todo, TodoCreate

async def create_todo(session: AsyncSession, todo_create: TodoCreate) -> Todo:
    """Tạo todo mới"""
    db_todo = Todo(
        title=todo_create.title,
        description=todo_create.description
    )
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    return db_todo

async def get_todos(session: AsyncSession) -> list[Todo]:
    """Lấy tất cả todos"""
    result = await session.execute(select(Todo))
    return result.scalars().all()

async def get_todo(session: AsyncSession, todo_id: int) -> Todo | None:
    """Lấy 1 todo theo id"""
    result = await session.execute(select(Todo).where(Todo.id == todo_id))
    return result.scalar_one_or_none()

async def update_todo(session: AsyncSession, todo_id: int, update_data: dict) -> Todo | None:
    """Cập nhật todo"""
    db_todo = await get_todo(session, todo_id)
    if not db_todo:
        return None
    
    for key, value in update_data.items():
        if value is not None:
            setattr(db_todo, key, value)
    
    await session.commit()
    await session.refresh(db_todo)
    return db_todo

async def delete_todo(session: AsyncSession, todo_id: int) -> bool:
    """Xóa todo"""
    db_todo = await get_todo(session, todo_id)
    if not db_todo:
        return False
    
    await session.delete(db_todo)
    await session.commit()
    return True