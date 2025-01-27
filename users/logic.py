from dataclasses import dataclass
from typing import List

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from users.auth.utils import pwd_context
from users.models import User
from users.schemas import UserCreateSchema, UserUpdateSchema


@dataclass
class UserLogic:
    db_session: AsyncSession

    async def get_user_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        async with self.db_session as session:
            result = (await session.execute(query)).scalar_one_or_none()
            return result

    async def get_all_users(self) -> List[User]:
        async with self.db_session as session:
            result = (await session.execute(select(User))).scalars().all()
            return result

    async def get_user_by_id(self, user_id: int) -> User | None:
        query = select(User).where(User.id == user_id)
        async with self.db_session as session:
            result = (await session.execute(query)).scalar_one_or_none()
            return result

    async def create_user(self, data: UserCreateSchema) -> User:
        query = (
            insert(User)
            .values(
                username=data.username,
                email=data.email,
                password=pwd_context.hash(data.password),
            )
            .returning(User)
        )

        async with self.db_session as session:
            new_user = (await session.execute(query)).scalar()
            await session.commit()

            return new_user

    async def change_user_password(self, user_id: int, password: str) -> User:
        query = select(User).where(User.id == user_id)
        async with self.db_session as session:
            new_user = (await session.execute(query)).scalar_one_or_none()
            new_user.password = pwd_context.hash(password)
            await session.commit()
            return new_user

    async def update_user(self, user_id: int, data: UserUpdateSchema) -> User:
        query = select(User).where(User.id == user_id)
        async with self.db_session as session:
            updated_user = (await session.execute(query)).scalar()
            if data.name:
                updated_user.name = data.name
            if data.surname:
                updated_user.surname = data.surname
            if data.phone_number:
                updated_user.phone_number = data.phone_number
            if data.email:
                updated_user.email = data.email
            await session.commit()
            return updated_user
