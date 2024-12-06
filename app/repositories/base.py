from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from fastapi.exceptions import HTTPException


class BaseRepository:
    model = None
    
    def __init__(self, session):
        self.session = session
        
    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_object_by_id(self, id):
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalars().one()
    
    async def add(self, data_object: BaseModel):
        add_model_stmt = insert(self.model).values(**data_object.model_dump()).returning(self.model)
        result = await self.session.execute(add_model_stmt)
        return result.scalars().one()
    
    async def delete(self, **filter_by):
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
        
    async def edit(self, object_data: BaseModel, exclude_unset: bool = False, **filter_by):
        update_stmt = (
            update(self.model).
            filter_by(**filter_by).
            values(**object_data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)
