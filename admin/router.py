import logging

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.requests import Request

from admin.logic import AdminLogic
from admin.service import AdminService
from dependency import get_user_logic, get_auth_service, get_admin_logic, get_admin_service
from exceptions import TokenNotCorrectException, AccessTokenNotFound, UserNotAdminException
from users.auth.service import AuthService
from users.logic import UserLogic

router = APIRouter(prefix='/admin', tags=['admin'])
logger = logging.getLogger(__name__)


@router.get('/get_user/{user_id}')
async def get_user(request: Request,
                   user_id: int,
                   admin_service: AdminService = Depends(get_admin_service),
                   user_logic: UserLogic = Depends(get_user_logic)):
    admin_service.check_admin_privileges(request)
    return await user_logic.get_user_by_id(user_id)


@router.get('/get_all_users')
async def get_all_users(request: Request,
                        admin_service: AdminService = Depends(get_admin_service),
                        user_logic: UserLogic = Depends(get_user_logic)):

    admin_service.check_admin_privileges(request)
    return await user_logic.get_all_users()



@router.post('/block_user/{user_id}')
async def block_user(request: Request,
                     user_id: int,
                     admin_logic: AdminLogic = Depends(get_admin_logic),
                     admin_service: AdminService = Depends(get_admin_service)
                     ):
    admin_service.check_admin_privileges(request)
    data = await admin_logic.block_user_by_user_id(user_id)
    return data