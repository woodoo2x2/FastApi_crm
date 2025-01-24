from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from clients.logic import ClientLogic
from infrastructure.database.config import get_db_session
from infrastructure.mail.service import MailService
from orders.logic import OrderLogic
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


def get_auth_service(user_logic: UserLogic = Depends(get_user_logic)):
    return AuthService(user_logic=user_logic)
