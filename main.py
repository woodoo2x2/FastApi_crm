from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from admin.router import router as admin_router
from crm.clients.router import router as client_router
from settings import Settings
from users.auth.router import router as auth_router

app = FastAPI()
settings = Settings()

app.include_router(client_router)
app.include_router(auth_router)
app.include_router(admin_router)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY,
    session_cookie="session",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "https://127.0.0.1:8000"],  # Укажите ваши домены
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    expose_headers=["*"],
)
