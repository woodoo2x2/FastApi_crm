from fastapi import Depends, security, Security, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from admin.logic import AdminLogic
from admin.service import AdminService
from crm.clients.logic import ClientLogic
from exceptions import TokenExpiredException, TokenNotCorrectException
from infrastructure.database.config import get_db_session
from infrastructure.mail.service import MailService
from crm.orders.logic import OrderLogic
from settings import Settings
from users.auth.service import AuthService
from users.logic import UserLogic


def get_settings():
    return Settings()


def get_orders_logic(db_session: AsyncSession = Depends(get_db_session)) -> OrderLogic:
    return OrderLogic(db_session=db_session)


def get_client_logic(db_session: AsyncSession = Depends(get_db_session)) -> ClientLogic:
    return ClientLogic(db_session=db_session)


def get_user_logic(db_session: AsyncSession = Depends(get_db_session)) -> UserLogic:
    return UserLogic(db_session=db_session)


def get_mail_service(settings: Settings = Depends(get_settings),
                     user_logic: UserLogic = Depends(get_user_logic)) -> MailService:
    return MailService(settings=settings, user_logic=user_logic)


def get_auth_service(user_logic: UserLogic = Depends(get_user_logic),
                     settings: Settings = Depends(get_settings)):
    return AuthService(user_logic=user_logic, settings=settings)


reusable_oauth2 = security.HTTPBearer()


def get_request_user_id(auth_service: AuthService = Depends(get_auth_service),
                        token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
                        ) -> int | None:
    try:
        user_id = auth_service.get_user_id_from_token(token.credentials)
    except TokenExpiredException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except TokenNotCorrectException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    return user_id


def get_admin_service(auth_service: AuthService = Depends(get_auth_service)):
    return AdminService(auth_service)


def get_admin_logic(db_session: AsyncSession = Depends(get_db_session),
                    user_logic: UserLogic = Depends(get_user_logic)):
    return AdminLogic(db_session=db_session, user_logic=user_logic)
