from sqlalchemy import select, func

from app.models.hotels import Hotels
from repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = Hotels
    
    async def get_all(
        self,
        title,
        location,
        limit,
        offset,
    ):
        query = select(Hotels)
        if title:
            query = query.where(
                func.lower(Hotels.title)
                .contains(title.strip().lower())
            )
        if location:
            query = query.where(
                func.lower(Hotels.location)
                .contains(location.strip().lower())
            ) 
        query = (
            query
            .limit(limit)
            .offset(offset)
        )     
        result = await self.session.execute(query)
        
        return result.scalars().all()