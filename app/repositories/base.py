from asyncpg import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from fastapi.exceptions import HTTPException

from app.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException
from app.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by) -> list[BaseModel]:
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(object) for object in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        try:
            item = result.scalars().one_or_none()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(item)
    
    async def get_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        try:
            item = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(item)

    async def add(self, data_object: BaseModel):
        add_model_stmt = insert(self.model).values(**data_object.model_dump()).returning(self.model)
        try:
            pre_result = await self.session.execute(add_model_stmt)
        except IntegrityError as e:
            if isinstance(e.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from e
            else:
                raise e
        result = pre_result.scalar_one()
        return result

    async def add_bulk(self, data_object: list[BaseModel]):
        add_model_stmt = insert(self.model).values([item.model_dump() for item in data_object])
        await self.session.execute(add_model_stmt)

    async def delete(self, **filter_by):
        delete_stmt = delete(self.model).filter_by(**filter_by)
        try:
            await self.session.execute(delete_stmt)
        except NoResultFound:
            raise ObjectNotFoundException

    async def delete_all(self):
        delete_stmt = delete(self.model)
        await self.session.execute(delete_stmt)

    async def edit(self, object_data: BaseModel, exclude_unset: bool = False, **filter_by):
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**object_data.model_dump(exclude_unset=exclude_unset))
        )
        try:
            await self.session.execute(update_stmt)
        except NoResultFound:
            raise ObjectNotFoundException
