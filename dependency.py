from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from clients.logic import ClientLogic
from database.db import get_db_session
from orders.logic import OrderLogic
from users.auth.service import AuthService
from users.logic import UserLogic


def get_orders_logic(db_session: AsyncSession = Depends(get_db_session)) -> OrderLogic:
    return OrderLogic(db_session=db_session)


def get_client_logic(db_session: AsyncSession = Depends(get_db_session)) -> ClientLogic:
    return ClientLogic(db_session=db_session)


def get_user_logic(db_session: AsyncSession = Depends(get_db_session)) -> UserLogic:
    return UserLogic(db_session=db_session)


def get_auth_service(user_logic: UserLogic = Depends(get_user_logic)):
    return AuthService(user_logic=user_logic)
