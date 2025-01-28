import json
from typing import List

from fastapi import APIRouter, Depends
from starlette.websockets import WebSocketDisconnect, WebSocket

from crm.orders.logic import OrderLogic
from crm.orders.schemas import OrderCreateSchema
from dependency import get_orders_logic
from exceptions import OrderNotFoundException

router = APIRouter(prefix='/kanban', tags=['kanban'])


class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = WebSocketManager()


@router.websocket("/ws/orders")
async def websocket_orders_endpoint(websocket: WebSocket,
                                    order_logic: OrderLogic = Depends(get_orders_logic)):
    await manager.connect(websocket)
    try:
        while True:
            # Получаем сообщение от клиента
            data = await websocket.receive_text()
            request = json.loads(data)

            action = request.get("action")
            response = {}

            if action == "create_order":
                # Создание заказа
                order_data = OrderCreateSchema(**request.get("data"))
                user_id = request.get("user_id", 0)  # Получите user_id из сообщения
                order = await order_logic.create_order(order_data, user_id)
                response = {"action": "order_created", "order": order}

            elif action == "get_all_orders":
                # Получение всех заказов
                orders = await order_logic.get_all_orders()
                response = {"action": "all_orders", "orders": orders}

            elif action == "get_order":
                # Получение заказа по ID
                order_id = request.get("order_id")
                try:
                    order = await order_logic.get_order_by_id(order_id)
                    response = {"action": "order_details", "order": order}
                except OrderNotFoundException:
                    response = {"action": "error", "message": f"Order with ID {order_id} not found"}

            elif action == "delete_order":
                # Удаление заказа
                order_id = request.get("order_id")
                try:
                    await order_logic.delete_order(order_id)
                    response = {"action": "order_deleted", "order_id": order_id}
                except OrderNotFoundException:
                    response = {"action": "error", "message": f"Order with ID {order_id} not found"}

            # Отправляем ответ клиенту
            await manager.broadcast(json.dumps(response))

    except WebSocketDisconnect:
        manager.disconnect(websocket)
