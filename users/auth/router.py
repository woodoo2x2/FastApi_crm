import logging

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from starlette import status

from dependency import get_auth_service, get_user_logic, get_mail_service
from exceptions import UserNotFoundException, UserNotCorrectPasswordException,    UserNotConfirmedByAdminException
from infrastructure.mail.service import MailService
from users.auth.service import AuthService
from users.logic import UserLogic
from users.schemas import UserLoginSchema, UserCreateSchema, ResetPasswordRequest

router = APIRouter(prefix='/auth', tags=['auth'])

logger = logging.getLogger(__name__)


@router.post("/login", name="login_post")
async def login_post(
        data: UserLoginSchema,
        auth_service: AuthService = Depends(get_auth_service),
):
    try:
        data = await auth_service.login(email=data.email, password=data.password)
        logger.info(f"Login successful")
        return data
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    except UserNotCorrectPasswordException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    except UserNotConfirmedByAdminException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)

@router.post("/registration")
async def registration_post(
        data: UserCreateSchema,
        user_logic: UserLogic = Depends(get_user_logic),
        background_tasks: BackgroundTasks = BackgroundTasks(),
        mail_service: MailService = Depends(get_mail_service)
):
    user = await user_logic.get_user_by_email(email=data.email)
    if user:
        logger.warning(f"Регистрация не удалась. Email {data.email} уже используется.")
        raise HTTPException(status_code=400, detail="Этот email уже используется.")
    new_user = await user_logic.create_user(
        UserCreateSchema(username=data.username, email=data.email, password=data.password))
    background_tasks.add_task(mail_service.send_confirmation_email, new_user)
    return {"message": f"user {new_user.email} created"}


@router.post("/recovery_password")
async def recovery_password_post(
        email: str,
        background_tasks: BackgroundTasks = BackgroundTasks(),
        mail_service: MailService = Depends(get_mail_service),
        user_logic: UserLogic = Depends(get_user_logic),
):
    logger.info(f"Попытка восстановления пароля для email: {email}.")
    user = await user_logic.get_user_by_email(email=email)
    if user:
        logger.info(f"Письмо для восстановления пароля отправлено на {email}.")
        background_tasks.add_task(mail_service.send_reset_password_email, user)
        return {"message": f"Письмо для восстановления пароля отправлено на {email}"}
    logger.warning(f"Восстановление пароля не удалось. Пользователь с email {email} не найден.")
    raise HTTPException(status_code=400, detail="Пользователь с таким email не найден.")


# POSTMAN content/type - application/json / body  {password: "password"}
@router.post("/reset_password/{token}")
async def reset_password_post(
        token: str,
        request: ResetPasswordRequest,
        mail_service: MailService = Depends(get_mail_service),
        user_logic: UserLogic = Depends(get_user_logic),
):
    logger.info("Обработка POST-запроса на смену пароля.")
    user = await mail_service.verify_reset_password_token(token)
    if not user:
        logger.error("Токен восстановления пароля неверный или просрочен.")
        raise HTTPException(status_code=400, detail="Неверный или просроченный токен.")
    await user_logic.change_user_password(user_id=user.id, password=request.password)
    logger.info(f"Пароль пользователя {user.email} успешно изменён.")
    return {'message': f'Пароль пользователя {user.email} успешно изменён.'}
