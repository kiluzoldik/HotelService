from sqlalchemy import select


class BaseRepository:
    model = None
    
    def __init__(self, session):
        self.session = session
        
    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
