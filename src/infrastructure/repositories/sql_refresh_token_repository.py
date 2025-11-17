from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain.models.refresh_token import RefreshToken, RefreshTokenBase
from domain.repositories.refresh_token_repository import RefreshTokenRepository
from infrastructure.orm.refresh_token_orm_model import RefreshTokenOrmModel
from fastapi import HTTPException
from datetime import datetime
from infrastructure.orm.orm_update_helper import update_orm_model_from_domain


class SQLRefreshTokenRepository(RefreshTokenRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all(self, current_user: dict) -> List[RefreshToken]:
        if current_user:
            result = await self.db_session.execute(select(RefreshTokenOrmModel).filter(RefreshTokenOrmModel.is_deleted.is_(False)))
            orm_refresh_token = result.scalars().all()
            refresh_token = [item.to_domain() for item in orm_refresh_token]
            return refresh_token

    async def add(self, refresh_token: RefreshToken, current_user: dict) -> bool:
        if current_user:
            refresh_token_result = await self.db_session.execute(select(RefreshTokenOrmModel).filter_by(refresh_token=refresh_token.refresh_token))
            orm_refresh_token = refresh_token_result.scalars().first()

            if orm_refresh_token:
                raise HTTPException(status_code=400, detail="RefreshToken with this name already exists")

            orm_refresh_token = RefreshTokenOrmModel.from_domain(refresh_token)
            await self.db_session.merge(orm_refresh_token)
            try:
                await self.db_session.commit()
                return True
            except SQLAlchemyError:
                await self.db_session.rollback()
                return False

    async def get_by_id(self, id: int, current_user: dict) -> RefreshToken:
        if current_user:
            result = await self.db_session.execute(
                select(RefreshTokenOrmModel).filter(RefreshTokenOrmModel.id == id, RefreshTokenOrmModel.is_deleted.is_(False)))
            orm_refresh_token = result.scalars().first()

            if orm_refresh_token is None:
                raise HTTPException(status_code=400, detail="Wrong RefreshToken")

            refresh_token = orm_refresh_token.to_domain()
            return refresh_token

    async def update_refresh_token(self, update_refresh_token: RefreshTokenBase, current_user: dict) -> bool:
        if current_user:
            result = await self.db_session.execute(
                select(RefreshTokenOrmModel).filter(RefreshTokenOrmModel.code == update_refresh_token.code, RefreshTokenOrmModel.is_deleted.is_(False)))
            orm_refresh_token = result.scalars().first()

            if orm_refresh_token is None:
                raise HTTPException(status_code=400, detail="Wrong RefreshToken")

            orm_refresh_token = update_orm_model_from_domain(orm_refresh_token, update_refresh_token)
            orm_refresh_token.updated_at = datetime.now()
            orm_refresh_token.updated_by = current_user["user"].id

            try:
                await self.db_session.commit()
                return True
            except SQLAlchemyError:
                await self.db_session.rollback()
                return False

    async def delete_refresh_token(self, id: int, current_user: dict) -> bool:
        if current_user:
            result = await self.db_session.execute(
                select(RefreshTokenOrmModel).filter(RefreshTokenOrmModel.id == id, RefreshTokenOrmModel.is_deleted.is_(False)))
            orm_refresh_token = result.scalars().first()

            if orm_refresh_token is None:
                raise HTTPException(status_code=400, detail="Wrong RefreshToken")

            orm_refresh_token.updated_at = datetime.now()
            orm_refresh_token.is_deleted = True
            orm_refresh_token.deleted_at = datetime.now()
            orm_refresh_token.deleted_by = current_user["user"].id
            try:
                await self.db_session.commit()
                return True
            except SQLAlchemyError:
                await self.db_session.rollback()
                return False