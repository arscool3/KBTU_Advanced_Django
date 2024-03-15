from fastapi import APIRouter

router = APIRouter(prefix='')

@router.get('', tags=['human'])
def get_human(db: Database) -> list[Human]:
    pass