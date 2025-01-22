from fastapi import APIRouter
from crm.kanban.router import router as kanban_router
router = APIRouter(prefix='/crm', tags=['crm'])

router.include_router(kanban_router)

@router.get('/')
async def crm_page():
    return {'message': 'crm_page'
            }
