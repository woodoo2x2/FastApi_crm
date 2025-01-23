from dataclasses import dataclass

from exceptions import UserNotFoundException, UserNotCorrectPasswordException
from users.auth.utils import pwd_context
from users.logic import UserLogic
from users.models import User
from users.schemas import UserLoginSchema, UserAuthSchema


@dataclass
class AuthService:
    user_logic: UserLogic

    async def login(self, email: str, password: str) -> UserAuthSchema:
        try:
            user = await self.user_logic.get_user_by_email(email)
            self._validate_user(user, password)
            return UserAuthSchema(user_id=user.id, email=user.email)
        except Exception as e:
            print(f"Error during login: {e}")
            raise

    @staticmethod
    def _validate_user(user: User, password: str):
        if not user:
            raise UserNotFoundException
        if not pwd_context.verify(password, user.password):
            raise UserNotCorrectPasswordException("Incorrect password.")
