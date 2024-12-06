from pydantic import BaseModel
from sqlalchemy import select, insert, delete
from fastapi.exceptions import HTTPException


class BaseRepository:
    model = None
    
    def __init__(self, session):
        self.session = session
        
    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def add(self, data_object: BaseModel):
        add_model_stmt = insert(self.model).values(**data_object.model_dump()).returning(self.model)
        result = await self.session.execute(add_model_stmt)
        return result.scalars().one()
    
    async def delete(self, object_id: int, message: str):
        object = await self.session.get(self.model, object_id)
        if not object:
            raise HTTPException(status_code=404, detail=f"{message}")
        await self.session.delete(object)
        await self.session.commit()
        
    async def edit(self, object_id: int, object_data: BaseModel, message: str):
        object = await self.session.get(self.model, object_id)
        if not object:
            raise HTTPException(status_code=404, detail=f"{message}")
        result = object_data.model_dump()
        for field, value in result.items():
            setattr(object, field, value)
        
        return object
        
        
        
