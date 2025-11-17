from api.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from application.use_cases.communication_use_cases import CommunicationUseCases
from application.use_cases.payment_use_cases import PaymentUseCases
from application.use_cases.reward_point_use_cases import RewardPointUseCases
from application.use_cases.store_credit_use_cases import StoreCreditUseCases
from application.use_cases.user_coupon_use_cases import UserCouponUseCases
from infrastructure.external.hq_adapter import HqAdapter
from infrastructure.external.paynow_adapter import PaynowAdapter
from infrastructure.helper.substition_cipher import SubstitutionCipher
from infrastructure.repositories.sql_coupon_definition_repository import SQLCouponDefinitionRepository
from infrastructure.repositories.sql_payment_method_repository import SQLPaymentMethodRepository
from infrastructure.repositories.sql_payment_repository import SQLPaymentRepository
from infrastructure.repositories.sql_reward_point_repository import SQLRewardPointRepository
from infrastructure.repositories.sql_store_credit_repository import SQLStoreCreditsRepository
from infrastructure.repositories.sql_transaction_repository import SQLTransactionRepository
from infrastructure.repositories.sql_user_coupon_repository import SQLUserCouponRepository
from infrastructure.repositories.sql_user_repository import SQLUserRepository
from infrastructure.repositories.sql_auth_repository import SQLAuthRepository
from infrastructure.repositories.sql_otp_repository import SQLOtpRepository
from infrastructure.external.twilio_sms_adapter import TwilioSmsAdapter
from application.use_cases.auth_use_cases import AuthUseCases
from application.use_cases.user_use_cases import UserUseCases
from application.use_cases.otp_use_cases import OtpUseCases
from infrastructure.repositories.sql_member_group_coupons_repository import SQLMemberGroupCouponsRepository
from infrastructure.repositories.sql_member_groups_repository import SQLMemberGroupsRepository
from infrastructure.repositories.sql_user_coupon_usage_repository import SQLUserCouponUsageRepository

# Dependency injection for UserUseCases

def get_user_use_cases(db: AsyncSession = Depends(get_db)) -> UserUseCases:
    user_repository = SQLUserRepository(db)
    auth_repository = SQLAuthRepository(db)
    otp_repository = SQLOtpRepository(db)
    cipher = SubstitutionCipher()
    hq_adapter = HqAdapter()
    return UserUseCases(user_repository, auth_repository, otp_repository, cipher, hq_adapter)

def get_user_coupon_use_cases(db: AsyncSession = Depends(get_db)) -> UserCouponUseCases:
    user_coupon_repository = SQLUserCouponRepository(db)
    coupon_definition_repository = SQLCouponDefinitionRepository(db)
    user_coupon_usage_repository = SQLUserCouponUsageRepository(db)
    member_group_coupon_repository = SQLMemberGroupCouponsRepository(db)
    member_group_repository = SQLMemberGroupsRepository(db)
    return UserCouponUseCases(user_coupon_repository, coupon_definition_repository, member_group_repository, member_group_coupon_repository, user_coupon_usage_repository)

    reward_point_repository = SQLRewardPointRepository(db)
    reward_point_service = RewardPointUseCases(reward_point_repository)
def get_reward_point_use_cases(db: AsyncSession = Depends(get_db)) -> RewardPointUseCases:
    reward_point_repository = SQLRewardPointRepository(db)
    reward_point_service = RewardPointUseCases(reward_point_repository)
    return reward_point_service

# Dependency injection for AuthUseCases
def get_auth_use_cases(db: AsyncSession = Depends(get_db)) -> AuthUseCases:
    auth_repository = SQLAuthRepository(db)
    otp_repository = SQLOtpRepository(db)
    return AuthUseCases(auth_repository, otp_repository)

# Dependency injection for OtpUseCases
def get_otp_use_cases(db: AsyncSession = Depends(get_db)) -> OtpUseCases:
    otp_repository = SQLOtpRepository(db)
    twilio_sms_adapter = TwilioSmsAdapter()
    return OtpUseCases(otp_repository, twilio_sms_adapter)

def get_communication_use_cases(db: AsyncSession = Depends(get_db)) -> CommunicationUseCases:
    twilio_sms_adapter = TwilioSmsAdapter()
    return CommunicationUseCases(twilio_sms_adapter)

def get_payment_use_cases(db: AsyncSession = Depends(get_db)) -> PaymentUseCases:

    payment_repository = SQLPaymentRepository(db)
    paynow_adapter = PaynowAdapter()
    transaction_repository = SQLTransactionRepository(db)
    payment_method_repository = SQLPaymentMethodRepository(db)

    payment_use_cases = PaymentUseCases(
        payment_repository=payment_repository,
        payment_adapter=paynow_adapter,
        transaction_repository=transaction_repository,
        payment_method_repository=payment_method_repository
    )

    return payment_use_cases

def get_store_credit_use_cases(db: AsyncSession = Depends(get_db)) -> StoreCreditUseCases:
    store_credit_repository = SQLStoreCreditsRepository(db)
    store_credit_use_cases = StoreCreditUseCases(store_credit_repository)

    return store_credit_use_cases
