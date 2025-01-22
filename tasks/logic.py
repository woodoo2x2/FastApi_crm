from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class TaskLogic:
    db_session: AsyncSession

    async def create_task(self, data: OrderCreateSchema) -> Order:
        pass

    async def update_task(self, data: OrderUpdateSchema) -> Order:
        pass

    async def delete_task(self, order_id:int) -> None:
        pass

    async def get_task_by_id(self, order_id:int) -> Order:
        pass

    async def get_all_tasks(self) -> list[Order] | None:
        pass
