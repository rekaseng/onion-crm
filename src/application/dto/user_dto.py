from typing import Optional, List

from pydantic import BaseModel

from domain.models.coupon_definition import CouponDefinition
from domain.models.full_coupon import FullCoupon
from domain.models.reward_point import RewardPointOption
from domain.models.user import User


class ProfileDto(BaseModel):
    id: Optional[int] = None
    mobile : Optional[str] =  None
    country_code : Optional[str] =  None
    full_mobile : Optional[str] =  None
    firstname : Optional[str] =  None
    lastname : Optional[str] =  None
    email : Optional[str] =  None
    birth_year : Optional[int] =  None
    birth_month : Optional[int] =  None
    email_consent : Optional[bool] = True
    sms_consent : Optional[bool] = True

    @staticmethod
    def from_domain(domain: User):
        return ProfileDto(
            id = domain.id,
            mobile = domain.mobile,
            country_code = domain.country_code,
            full_mobile = domain.full_mobile,
            firstname = domain.firstname,
            lastname = domain.lastname,
            email = domain.email,
            birth_year = domain.birth_year,
            birth_month = domain.birth_month,
            email_consent = domain.email_consent,
            sms_consent = domain.sms_consent
        )


class UserAdjustWalletDto(BaseModel):
    customer_id: Optional[int] = None
    amount: Optional[float] = None
    description: Optional[str] = None

class MachineLoginDto(BaseModel):
    session_ref: Optional[str]= None
    session_id: Optional[str] = None
    machine_id: Optional[int] =None

class MachineLoginWithUserDto(BaseModel):
    machine_id: Optional[int] = None
    session_ref: Optional[str] = None
    user_id: Optional[int] = None
    saved_credit_card: Optional[int] = None
    stored_credits: Optional[str] = None
    user_qr_string: Optional[str] = None


class MachineUserCouponDto(BaseModel):
    id: Optional[int] = None
    name: str
    code: str
    discount_type: str
    discount_amount: float
    minimum_spending: Optional[float] = None
    minimum_spending_active: bool
    criterial_cart_type: Optional[str] = None
    criterial_cart_skus: List[int]
    criterial_cart_collections: List[int]
    target_type: str
    target_skus: List[int]
    target_collections: List[int]
    user_coupon_id: Optional[int] = None
    member_group_coupon_id: Optional[int] = None

    @staticmethod
    def from_domain(domain: FullCoupon):
        data = MachineUserCouponDto(
            id = domain.id,
            name = domain.name,
            code = domain.code,
            discount_type = domain.discount_type,
            discount_amount = domain.discount_amount,
            minimum_spending = domain.minimum_spending,
            minimum_spending_active = domain.minimum_spending_active,
            criterial_cart_type = domain.criterial_cart_type,
            criterial_cart_skus = domain.criterial_cart_skus,
            criterial_cart_collections = domain.criterial_cart_collections,
            target_type = domain.target_type,
            target_skus = domain.target_skus,
            target_collections = domain.target_collections,
            user_coupon_id = domain.user_coupon_id,
            member_group_coupon_id = domain.member_group_coupon_id
        )

        return data

# class MachineUserRewardPointDto(BaseModel):
#     point: Optional[int] = None
#     discount: Optional[float] = None

class MachineUserBasicDto(BaseModel):
    firstname: str

class MachineUserRewardDto(BaseModel):
    user: MachineUserBasicDto
    coupons: List[MachineUserCouponDto]
    reward_points: List[RewardPointOption]