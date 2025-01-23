import logging

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.requests import Request

from dependency import get_auth_service, get_user_logic
from exceptions import UserNotFoundException, UserNotCorrectPasswordException
from users.auth.service import AuthService
from users.logic import UserLogic
from users.schemas import UserLoginSchema, UserCreateSchema

router = APIRouter(prefix='/auth', tags=['auth'])

logger = logging.getLogger(__name__)

@router.post("/login", name="login_post")
async def login_post(
        request: Request,
        data: UserLoginSchema,
        auth_service: AuthService = Depends(get_auth_service),
):
    try:
        user = await auth_service.login(email=data.email, password=data.password)
        request.session["user_id"] = user.user_id
        request.session["email"] = user.email
        return {"message": f"user with {user.email} login"}
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    except UserNotCorrectPasswordException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)

@router.post("/registration")
async def registration_post(
        data : UserCreateSchema,
        user_logic: UserLogic = Depends(get_user_logic),
):
    logger.info(f"Попытка регистрации нового пользователя с email: {data.email}.")
    user = await user_logic.get_user_by_email(email=data.email)
    if user:
        logger.warning(f"Регистрация не удалась. Email {data.email} уже используется.")
        raise HTTPException(status_code=400, detail="Этот email уже используется.")
    new_user = await user_logic.create_user(UserCreateSchema(username=data.username, email=data.email, password=data.password))
    logger.info(f"Пользователь {new_user.email} успешно зарегистрирован.")

    return {"message": f"user {new_user.email} created"}
