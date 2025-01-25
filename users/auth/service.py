from dataclasses import dataclass
from datetime import datetime, timedelta

from jose import jwt

from exceptions import UserNotFoundException, UserNotCorrectPasswordException, TokenNotCorrectException, \
    TokenExpiredException
from settings import Settings
from users.auth.utils import pwd_context
from users.logic import UserLogic
from users.models import User
from users.schemas import UserAuthSchema, UserAuthenticatedSchema


@dataclass
class AuthService:
    user_logic: UserLogic
    settings: Settings

    async def login(self, email: str, password: str) -> UserAuthenticatedSchema:
        try:
            user = await self.user_logic.get_user_by_email(email)
            self._validate_user(user, password)
            access_token = self.generate_access_token(user.id)
            return UserAuthenticatedSchema(user_id=user.id, access_token=access_token)
        except Exception as e:
            raise UserNotFoundException

    @staticmethod
    def _validate_user(user: User, password: str):
        if not user:
            raise UserNotFoundException
        if not pwd_context.verify(password, user.password):
            raise UserNotCorrectPasswordException("Incorrect password.")

    def generate_access_token(self, user_id: int):
        expire_time_unix = (datetime.utcnow() + timedelta(days=7)).timestamp()
        token = jwt.encode({'user_id': user_id, 'expire': expire_time_unix},
                           self.settings.JWT_SECRET_KEY,
                           algorithm=self.settings.JWT_DECODE_ALGORITHM)
        return token

    def get_user_id_from_token(self,token: str) -> int:
        try:
            payload = jwt.decode(token, self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_DECODE_ALGORITHM])
        except:
            raise TokenNotCorrectException
        if payload['expire'] > (datetime.utcnow() + timedelta(days=7)).timestamp():
            raise TokenExpiredException
        return payload['user_id']