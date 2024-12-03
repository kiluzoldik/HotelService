from sqlalchemy import select, insert


class BaseRepository:
    model = None
    
    def __init__(self, session):
        self.session = session
        
    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def add(self, data_object):
        print(data_object)
        add_hotel_stmt = insert(self.model).values(**data_object.model_dump())
        await self.session.execute(add_hotel_stmt)
        return data_object
