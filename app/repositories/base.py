from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from fastapi.exceptions import HTTPException


class BaseRepository:
    model = None
    schema: BaseModel = None
    
    def __init__(self, session):
        self.session = session
        
    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(
            object, 
            from_attributes=True
        ) for object in result.scalars().all()]
        
    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()
        
    async def get_one_or_none(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        item = result.scalars().one_or_none()
        if item is None:
            raise HTTPException(status_code=404, detail="Объект не найден")
        return self.schema.model_validate(item, from_attributes=True)
    
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
