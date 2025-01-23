from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from users.auth.router import router as auth_router
from clients.router import router as client_router
from crm.router import router as crm_router
from settings import Settings

app = FastAPI()
settings = Settings()


app.include_router(crm_router)
app.include_router(client_router)
app.include_router(auth_router)

app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY, max_age=1800)


@app.get('/')
async def main():
    return {"message": "homepage"}
