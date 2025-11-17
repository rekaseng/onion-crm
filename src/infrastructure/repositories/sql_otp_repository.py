from typing import List
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain.models.otp import Otp
from domain.repositories.otp_repository import OtpRepository
from infrastructure.orm.otp_orm_model import OtpOrmModel
from fastapi import HTTPException
from datetime import datetime, timedelta

from infrastructure.orm.orm_update_helper import update_orm_model_from_domain

class SQLOtpRepository(OtpRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add(self, otp: Otp) -> None:
        now = datetime.utcnow()

        recent_result = await self.db_session.execute(select(OtpOrmModel).filter(
            OtpOrmModel.full_mobile == otp.full_mobile,
            OtpOrmModel.created_at >= now - timedelta(seconds=30)
        ))

        recent_otp = recent_result.scalars().first()

        if recent_otp:
            raise HTTPException(status_code=400, detail="Please wait 30 seconds before requesting a new OTP.")

        last_hour_result = await self.db_session.execute(select(OtpOrmModel).filter(
            OtpOrmModel.full_mobile == otp.full_mobile,
            OtpOrmModel.created_at >= now - timedelta(hours=1)
        ))
        otp_last_hour_result = last_hour_result.scalars().all()

        if len(otp_last_hour_result) >= 5:
            raise HTTPException(status_code=400,
                                detail="Too many OTP requests. Please wait 1 hour and try again.")
        ###OLD OTP logic###

        # result = await self.db_session.execute(select(OtpOrmModel).filter(
        #     OtpOrmModel.full_mobile == otp.full_mobile,
        #     OtpOrmModel.created_at >= now - timedelta(minutes=5)
        # ))
        # orm_otp = result.scalars().first()
        #
        # if orm_otp:
        #     if orm_otp.attempts <= 5:
        #         raise HTTPException(status_code=400, detail="This mobile OTP already exists. Please check your otp.")
        #     if orm_otp.created_at >= now - timedelta(minutes=5):
        #         raise HTTPException(status_code=400,
        #                             detail="This mobile OTP already exists. Please retry in 5 minutes.")

        else:
            orm_otp = OtpOrmModel.from_domain(otp)
            self.db_session.add(orm_otp)

        await self.db_session.commit()

    async def verify(self, full_mobile: str, otp: str) -> bool :
        result = await self.db_session.execute(select(OtpOrmModel).filter(
            OtpOrmModel.full_mobile == full_mobile
        ).order_by(OtpOrmModel.created_at.desc()).limit(1))

        latest_otp = result.scalars().first()
        if not latest_otp:
            raise HTTPException(status_code=400, detail="Please request OTP")

        if latest_otp.otp != otp:
            if latest_otp.attempts >= 5:
                raise HTTPException(status_code=400,
                                    detail="Attempt exceeded. Please try to request new OTP after 5 minutes")

            latest_otp.attempts += 1
            await self.db_session.commit()
            raise HTTPException(status_code=400, detail="Incorrect OTP")

        return True





