from sqlalchemy.ext.asyncio import AsyncSession

from application.dto.auth_dto import UserAuthDTO
from infrastructure.db.session import SessionLocal
from fastapi import Depends, HTTPException, status
from utils import security
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from pydantic import ValidationError
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from infrastructure.repositories.sql_auth_repository import SQLAuthRepository
from infrastructure.repositories.sql_user_repository import SQLUserRepository
from infrastructure.repositories.sql_otp_repository import SQLOtpRepository
from infrastructure.repositories.sql_role_repository import SQLRoleRepository
from infrastructure.repositories.sql_tenant_repository import SQLTenantRepository
from infrastructure.repositories.sql_permission_repository import SQLPermissionRepository
from domain.models.login import TokenPayload
from application.use_cases.user_use_cases import UserUseCases
from application.use_cases.role_use_cases import RoleUseCases
from application.use_cases.tenant_use_cases import TenantUseCases
from application.use_cases.permission_use_cases import PermissionUseCases
from config import settings


reusable_oauth2 = HTTPBearer()


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


async def get_current_user_auth(
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(reusable_oauth2)
)-> UserAuthDTO:
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=["HS256"]
        )
        token_data = TokenPayload(**payload)
        user_repository = SQLUserRepository(db)
        auth_repository = SQLAuthRepository(db)
        otp_repository = SQLOtpRepository(db)
        user_service = UserUseCases(user_repository, auth_repository, otp_repository)
        user = await user_service.get_by_id(token_data.sub)

        if not user:
            raise HTTPException(status_code=400, detail="Authorization Error")

        role_repository = SQLRoleRepository(db)
        role_service = RoleUseCases(role_repository)
        role = await role_service.get_by_id(token_data.role_id, user)

        if not role:
            raise HTTPException(status_code=400, detail="Wrong Role")

        tenant_repository = SQLTenantRepository(db)
        tenant_service = TenantUseCases(tenant_repository)
        tenant = await tenant_service.get_by_id(token_data.tenant_id, user)
        user_auth = UserAuthDTO(
            user = user,
            role = role,
            tenant = tenant

        )

        return user_auth

    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials")

async def get_current_user(db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(reusable_oauth2)):
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=["HS256"]
        )
        token_data = TokenPayload(**payload)
        user_repository = SQLUserRepository(db)
        auth_repository = SQLAuthRepository(db)  # Added auth repository
        otp_repository = SQLOtpRepository(db)
        user_service = UserUseCases(user_repository, auth_repository, otp_repository)

        user = await user_service.get_by_id(token_data.sub)

        if not user:
            raise HTTPException(status_code=400, detail="Wrong User")

        role_repository = SQLRoleRepository(db)
        role_service = RoleUseCases(role_repository)
        role = await role_service.get_by_id(token_data.role_id, user)

        if not role:
            raise HTTPException(status_code=400, detail="Wrong Role")

        tenant_repository = SQLTenantRepository(db)
        tenant_service = TenantUseCases(tenant_repository)
        tenant = await tenant_service.get_by_id(token_data.tenant_id, user)

        return {"user": user, "role": role, "tenant": tenant}

    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials")


async def get_current_user_permissions(db: Session = Depends(get_db),
                                       current_user: dict = Depends(get_current_user)):
    role = current_user["role"]
    permissions = role.permissions

    # pass the list of permissions ids to permission service to verify
    permission_repository = SQLPermissionRepository(db)
    permission_service = PermissionUseCases(permission_repository)
    permission = await permission_service.get_by_permission(permissions)
    if not permission:
        raise HTTPException(status_code=400, detail="Wrong Permission")

    permission_names = [perm.name for perm in permission]

    return permission_names


def check_permission(required_permission: str):
    def permission_checker(permissions: list = Depends(get_current_user_permissions)):
        if required_permission not in permissions:
            raise HTTPException(status_code=400, detail="Insufficient permissions")
        return True

    return permission_checker


async def get_hq_admin(current_user: dict = Depends(get_current_user)):
    if not current_user["role"].is_hq_admin:
        raise HTTPException(status_code=400, detail="Insufficient permissions")
    return True


async def get_admin(current_user: dict = Depends(get_current_user)):
    if not current_user["role"].is_admin:
        raise HTTPException(status_code=400, detail="Insufficient permissions")
    return True


async def get_current_active_user(
        current_user: Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
        current_user: Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
