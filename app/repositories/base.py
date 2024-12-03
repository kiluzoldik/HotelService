from pydantic import BaseModel
from sqlalchemy import select, insert


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
