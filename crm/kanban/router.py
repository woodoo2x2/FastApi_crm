from fastapi import APIRouter

router = APIRouter(prefix='kanban')


@router.get('/')
def kanban_page():
    return {'message': 'kanban_page'}
