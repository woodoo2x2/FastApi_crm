import logging

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.requests import Request

from dependency import get_user_logic, get_auth_service
from exceptions import TokenNotCorrectException, AccessTokenNotFound, UserNotAdminException
from users.auth.service import AuthService
from users.logic import UserLogic

router = APIRouter(prefix='/admin', tags=['admin'])
logger = logging.getLogger(__name__)


@router.get('/get_user/{user_id}')
async def get_user(request: Request,
                   user_id: int,
                   auth_service: AuthService = Depends(get_auth_service),
                   user_logic: UserLogic = Depends(get_user_logic)):
    try:
        auth_service.user_is_admin_(request)
        logger.info("admin auth is ok")
        return await user_logic.get_user_by_id(user_id)
    except TokenNotCorrectException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail,
        )
    except AccessTokenNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail,
        )
    except UserNotAdminException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.detail,
        )


@router.get('/get_all_users')
async def get_all_users(request: Request,
                        auth_service: AuthService = Depends(get_auth_service),
                        user_logic: UserLogic = Depends(get_user_logic)):
    try:
        auth_service.user_is_admin_(request)
        logger.info("admin auth is ok")
        return await user_logic.get_all_users()
    except TokenNotCorrectException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail,
        )
    except AccessTokenNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail,
        )
    except UserNotAdminException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.detail,
        )
