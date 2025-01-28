import datetime
from dataclasses import dataclass
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crm.orders.models import Order
from crm.orders.schemas import OrderCreateSchema
from exceptions import OrderNotFoundException


@dataclass
class OrderLogic:
    db_session: AsyncSession

    async def create_order(self, data: OrderCreateSchema, user_id: int) -> Order:
        async with self.db_session as session:
            order = Order(
                name=data.name,
                description=data.description,
                date_of_creation=datetime.datetime.utcnow(),
                date_of_send=datetime.datetime.utcnow() + datetime.timedelta(days=2),
                address=data.address,
                delivery_method=data.delivery_method,
                client_id=1,
                price=data.price,

                author_id=user_id,
                responsable_id=user_id,
            )

            session.add(order)
            await session.commit()
            return order

    async def get_all_orders(self) -> Sequence[Order]:
        async with self.db_session as session:
            query = select(Order)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_order_by_id(self, order_id: int):
        async with self.db_session as session:
            query = select(Order).where(Order.id == order_id)
            result = await session.execute(query)
            return result.scalar()

    async def delete_order(self, order_id: int):
        order = await self.get_order_by_id(order_id)
        if not order:
            raise OrderNotFoundException
        if order.id == order_id:
            async with self.db_session as session:
                user = await session.scalar(select(Order).where(Order.id == order_id))
                await session.delete(user)
                await session.commit()
