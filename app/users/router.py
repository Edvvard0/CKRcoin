from fastapi import APIRouter


router = APIRouter(prefix='/users', tags=['Users'])


# @router.get('/profile')
# def get_users(tg_id: int):
#     return {'message': 'Конкретный юзер'}


