from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from crm.clients.logic import ClientLogic
from crm.clients.schemas import ClientCreateSchema
from dependency import get_client_logic
from exceptions import ClientNotFoundException

router = APIRouter(prefix='/clients', tags=['clients'])


@router.post('/')
async def create_client(data: ClientCreateSchema,
                        client_logic: ClientLogic = Depends(get_client_logic)):
    return await client_logic.create_client(data)


@router.get('/')
async def get_all_clients(client_logic: ClientLogic = Depends(get_client_logic)):
    return await client_logic.get_all_clients()


@router.get('/{client_id}')
async def get_client_by_id(client_id: int,
                           client_logic: ClientLogic = Depends(get_client_logic)):
    return await client_logic.get_client_by_id(client_id)


@router.delete('/{client_id}')
async def delete_client(client_id: int,
                        client_logic: ClientLogic = Depends(get_client_logic)):
    try:
        await client_logic.delete_client(client_id)
    except ClientNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
