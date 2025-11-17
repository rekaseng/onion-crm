from fastapi import APIRouter

from api.endpoints import (
    auth_endpoint,
    user_endpoint,
    coupon_endpoint,
    sku_endpoint,
    role_endpoint,
    tenant_endpoint,
    user_role_endpoint,
    store_credits_endpoint,
    orders_endpoint,
    member_groups_endpoint,
    member_group_users_endpoint,
    member_group_coupons_endpoint,
    payment_endpoint,
    transaction_endpoint,
    payment_method_endpoint
)

from api.endpoints.admin import (
    coupon_admin_endpoint,
    coupon_definition_admin_endpoint,
    user_coupon_admin_endpoint,
    member_groups_admin_endpoint,
    member_group_users_admin_endpoint,
    member_group_coupons_admin_endpoint,
    orders_admin_endpoint,
    role_admin_endpoint,
    user_admin_endpoint,
    machines_endpoint,
    machine_contracts_endpoint,
    permissions_endpoint, reward_point_endpoint, reward_rule_endpoint, payment_admin_endpoint, sku_admin_endpoint, store_credit_admin_endpoint
)

api_router = APIRouter()
admin_api_router = APIRouter()

api_router.include_router(auth_endpoint.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(user_endpoint.router, prefix="/users", tags=["Users"])
api_router.include_router(role_endpoint.router, prefix="/roles", tags=["Roles"])
api_router.include_router(user_role_endpoint.router, prefix="/user_role", tags=["UserRoles"])
api_router.include_router(tenant_endpoint.router, prefix="/tenants", tags=["Tenants"])
api_router.include_router(transaction_endpoint.router, prefix="/transactions", tags=["Transactions"])
api_router.include_router(coupon_endpoint.router, prefix="/coupons", tags=["Coupons"])
api_router.include_router(sku_endpoint.router, prefix="/skus", tags=["Skus"])
api_router.include_router(store_credits_endpoint.router, prefix="/store_credits", tags=["StoreCredits"])
api_router.include_router(orders_endpoint.router, prefix="/orders", tags=["Orders"])
api_router.include_router(member_groups_endpoint.router, prefix="/member_groups", tags=["MemberGroups"])
api_router.include_router(member_group_users_endpoint.router, prefix="/member_group_users", tags=["MemberGroupUsers"])
api_router.include_router(member_group_coupons_endpoint.router, prefix="/member_group_coupons", tags=["MemberGroupCoupons"])
api_router.include_router(payment_endpoint.router, prefix="/payment", tags=["Payment"])
api_router.include_router(payment_method_endpoint.router, prefix="/payment_method", tags=["PaymentMethod"])

admin_api_router.include_router(reward_point_endpoint.router, prefix="/reward_point", tags=["Admin RewardPoints"])
admin_api_router.include_router(reward_rule_endpoint.router, prefix="/reward_rule", tags=["Admin RewardRules"])
admin_api_router.include_router(coupon_admin_endpoint.router, prefix="/coupons", tags=["Admin Coupons"])
admin_api_router.include_router(coupon_definition_admin_endpoint.router, prefix="/couponDefinitions", tags=["Admin Coupon Definitions"])
admin_api_router.include_router(user_coupon_admin_endpoint.router, prefix="/userCoupons", tags=["Admin User Coupons"])
admin_api_router.include_router(member_groups_admin_endpoint.router, prefix="/member_groups",
                                tags=["Admin MemberGroups"])
admin_api_router.include_router(member_group_users_admin_endpoint.router, prefix="/member_group_users",
                                tags=["Admin MemberGroupUsers"])
admin_api_router.include_router(member_group_coupons_admin_endpoint.router, prefix="/member_group_coupons",
                                tags=["Admin MemberGroupCoupons"])
admin_api_router.include_router(orders_admin_endpoint.router, prefix="/orders", tags=["Admin Orders"])
admin_api_router.include_router(role_admin_endpoint.router, prefix="/roles", tags=["Admin Roles"])
admin_api_router.include_router(user_admin_endpoint.router, prefix="/users", tags=["Admin Users"])
admin_api_router.include_router(machines_endpoint.router, prefix="/machines", tags=["Admin Machines"])
admin_api_router.include_router(machine_contracts_endpoint.router, prefix="/machine_contracts", tags=["Admin MachineContracts"])
admin_api_router.include_router(permissions_endpoint.router, prefix="/permissions", tags=["Admin Permissions"])
admin_api_router.include_router(payment_admin_endpoint.router, prefix="/payments", tags=["Admin Payments"])
admin_api_router.include_router(sku_admin_endpoint.router, prefix="/admin-sku", tags=["Admin Skus"])
admin_api_router.include_router(store_credit_admin_endpoint.router, prefix="/store_credit", tags=["Admin StoreCredits"])