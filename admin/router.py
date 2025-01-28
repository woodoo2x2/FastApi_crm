import logging

from fastapi import APIRouter, Depends
from starlette.requests import Request

from admin.logic import AdminLogic
from admin.schemas import ChangeUserStatusSchema
from admin.service import AdminService
from dependency import get_user_logic, get_admin_logic, get_admin_service
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


@router.post('/change_user_status')
async def block_user(request: Request,
                     data: ChangeUserStatusSchema,
                     admin_logic: AdminLogic = Depends(get_admin_logic),
                     admin_service: AdminService = Depends(get_admin_service)
                     ):
    admin_service.check_admin_privileges(request)
    data = await admin_logic.change_user_status(data.user_id, data.status)
    return data
