from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from dependency import get_is_admin_and_user_id, get_user_logic
from users.logic import UserLogic

router = APIRouter(prefix='/admin', tags=['admin'])


@router.get('/get_user')
async def get_user(admin_and_user_id: list = Depends(get_is_admin_and_user_id),
                   user_logic: UserLogic = Depends(get_user_logic)):
    is_admin, user_id = admin_and_user_id
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return await user_logic.get_user_by_id(user_id)
