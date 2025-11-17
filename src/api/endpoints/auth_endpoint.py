from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import RedirectResponse

from application.dto.auth_dto import RegisterDTO, NewPasswordDTO, UserLoginDTO, SendOtpDto
from api.deps import get_current_user
from application.dto.user_dto import ProfileDto
from db_error_handlers import handle_db_errors
from api.di import get_user_use_cases, get_auth_use_cases, get_otp_use_cases
from application.use_cases.auth_use_cases import AuthUseCases
from application.use_cases.user_use_cases import UserUseCases
from application.use_cases.otp_use_cases import OtpUseCases

router = APIRouter()

@router.get("/redirect")
async def redirect_to_external():
    # Redirect to an external domain
    return RedirectResponse(url="https://members.shakesalad.com/login")


@router.post("/sign_up", response_model=dict)
@handle_db_errors
async def sign_up(
    register_dto: RegisterDTO,
    user_use_cases: UserUseCases = Depends(get_user_use_cases)
):
    register_response = await user_use_cases.sign_up(register_dto)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": {
            "user": register_response["user"].dict(),
            "access_token": register_response["token"].access_token
        }
    }

@router.post("/login", response_model=dict)
async def login_access_token(
    form_data: UserLoginDTO,
    auth_use_cases: AuthUseCases = Depends(get_auth_use_cases)
):
    new_login = await auth_use_cases.login_access_token(form_data)
    if not new_login.access_token:
        raise HTTPException(status_code=400, detail="Wrong User")
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "access_token": new_login.access_token
    }

@router.post("/validate", response_model=dict)
@handle_db_errors
async def user_token(current_user: dict = Depends(get_current_user)):
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": [current_user]
    }

@router.post("/new_reset_password", response_model=dict)
@handle_db_errors
async def reset_password(
    body: NewPasswordDTO,
    auth_use_cases: AuthUseCases = Depends(get_auth_use_cases)
):
    message = await auth_use_cases.reset_password(body.full_mobile, body.otp, body.new_password)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": message
    }

@router.get("/profile", response_model=dict)
@handle_db_errors
async def auth_profile(
    current_user: dict = Depends(get_current_user),
    user_use_cases: UserUseCases = Depends(get_user_use_cases)
):
    user = await user_use_cases.get_profile(current_user)
    profile = ProfileDto.from_domain(user)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": profile
    }

@router.post("/auth/send_otp", response_model=dict)#deprecated
async def send_otp(
    obj_in: SendOtpDto,
    otp_use_cases: OtpUseCases = Depends(get_otp_use_cases)
):
    otp = await otp_use_cases.send_otp(obj_in.full_mobile)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }

@router.post("/auth/send_otp_for_signup", response_model=dict)#deprecated
async def send_otp_for_signup(
    obj_in: SendOtpDto,
    otp_use_cases: OtpUseCases = Depends(get_otp_use_cases),
    user_use_cases: UserUseCases = Depends(get_user_use_cases)
):
    user = await user_use_cases.get_by_full_mobile(obj_in.full_mobile)

    if user:
        raise HTTPException(status_code=400, detail="You already have account. Please login")

    otp = await otp_use_cases.send_otp(obj_in.full_mobile)

    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": True
    }


@router.post("/send_otp", response_model=dict)
async def send_otp(
    obj_in: SendOtpDto,
    otp_use_cases: OtpUseCases = Depends(get_otp_use_cases)
):
    otp = await otp_use_cases.send_otp(obj_in.full_mobile)
    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": []
    }

@router.post("/send_otp_for_signup", response_model=dict)
async def send_otp_for_signup(
    obj_in: SendOtpDto,
    otp_use_cases: OtpUseCases = Depends(get_otp_use_cases),
    user_use_cases: UserUseCases = Depends(get_user_use_cases)
):
    user = await user_use_cases.get_by_full_mobile(obj_in.full_mobile)

    if user:
        raise HTTPException(status_code=400, detail="You already have account. Please login")

    otp = await otp_use_cases.send_otp(obj_in.full_mobile)

    return {
        "error_message": None,
        "success": True,
        "error_code": None,
        "result": True
    }
