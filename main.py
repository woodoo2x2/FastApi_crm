from fastapi import FastAPI

from clients.router import router as client_router
from settings import Settings
from users.auth.router import router as auth_router

app = FastAPI()
settings = Settings()

app.include_router(client_router)
app.include_router(auth_router)


@app.get('/')
async def main():
    return {"message": "homepage"}
