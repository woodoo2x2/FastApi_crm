from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from dependency import get_orders_logic
from exceptions import OrderNotFoundException
from orders.logic import OrderLogic
from orders.schemas import OrderCreateSchema

router = APIRouter(prefix='/kanban', tags=['kanban'])


@router.post('/')
async def create_order(data: OrderCreateSchema,
                       order_logic: OrderLogic = Depends(get_orders_logic)):
    return await order_logic.create_order(data)


@router.get('/')
async def get_all_orders(order_logic: OrderLogic = Depends(get_orders_logic)):
    return await order_logic.get_all_orders()


@router.get('/{order_id}')
async def get_order(order_id: int,
                    order_logic: OrderLogic = Depends(get_orders_logic)):
    return await order_logic.get_order_by_id(order_id)


@router.delete('/{order_id}')
async def delete_order(order_id: int,
                       order_logic: OrderLogic = Depends(get_orders_logic)):
    try:
        await order_logic.delete_order(order_id)
    except OrderNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
