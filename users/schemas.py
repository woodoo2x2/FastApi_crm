from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserAuthSchema(BaseModel):
    user_id: int
    email: str


class UserAuthenticatedSchema(BaseModel):
    user_id: int
    access_token: str


class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str


class UserUpdateSchema(BaseModel):
    name: str | None = None
    surname: str | None = None
    phone_number: str | None = None
    email: str | None = None


class ResetPasswordRequest(BaseModel):
    password: str
