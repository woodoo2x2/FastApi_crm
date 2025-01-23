from fastapi import FastAPI
from crm.router import router as crm_router
from clients.router import router as client_router
app = FastAPI()

app.include_router(crm_router)
app.include_router(client_router)

@app.get('/')
async def main():
    return {"message": "homepage"}
