from fastapi import APIRouter

router = APIRouter(prefix='/crm')


@router.get('/')
async def crm_page():
    return {'message': 'crm_page'
            }
