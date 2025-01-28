from dataclasses import dataclass
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crm.clients.models import Client
from crm.clients.schemas import ClientCreateSchema
from exceptions import ClientNotFoundException


@dataclass
class ClientLogic:
    db_session: AsyncSession

    async def create_client(self, data: ClientCreateSchema) -> Client:
        async with self.db_session as session:
            client = Client(
                name=data.name,
                surname=data.surname,
                phone_number=data.phone_number,
                inn=data.inn
            )
            session.add(client)
            await session.commit()
            return client

    async def get_all_clients(self) -> Sequence[Client]:
        async with self.db_session as session:
            query = select(Client)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_client_by_id(self, client_id: int):
        async with self.db_session as session:
            query = select(Client).where(Client.id == client_id)
            result = await session.execute(query)
            return result.scalar()

    async def delete_client(self, client_id: int):
        client = await self.get_client_by_id(client_id)
        if not client:
            raise ClientNotFoundException
        if client.id == client_id:
            async with self.db_session as session:
                user = await session.scalar(select(Client).where(Client.id == client_id))
                await session.delete(user)
                await session.commit()
