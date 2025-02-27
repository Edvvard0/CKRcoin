from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import selectinload

from app.database import SessionDep, get_session
from app.events.dao import EventParticipatedDAO
from app.events.router import get_event_by_id
from app.users.dao import UserDAO
from app.users.model import User
from app.users.schemas import SUser, SUserAdd, SUserUpdate, TelegramIDModel, UserIDModel

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/all_users')
async def get_all_users(session: SessionDep) -> list[SUser]:
    return await UserDAO.find_all(session)


@router.get('/profile')
async def get_profile(tg_id: int, session: SessionDep):
    return await UserDAO.find_one_or_none(session,
                                          options=[selectinload(User.events)],
                                          **{'tg_id': tg_id})


@router.get('/top_10')
async def get_top_users(session: SessionDep):
    return await UserDAO.find_top_users(session)


@router.get('/users_by_group')
async def get_users_by_group(session: SessionDep, group_id: int) -> List[SUser]:
    return await UserDAO.find_all(session, **{'group_id': group_id, 'role_id': 1})


@router.get('/users_my_group')
async def get_users_my_group(session: SessionDep, user: SUser = Depends(get_profile)) -> List[SUser]:
    """
    Мне кажется этот метод надо объединить с методом get_users_by_group
    """
    return await UserDAO.find_all(session, **{'group_id': user.group_id, 'role_id': 1})


@router.get('/portfolio')
async def get_portfolio(session: SessionDep, tg_id: int, user=Depends(get_profile)):
    # await session.refresh(user, options=[selectinload(User.events)])
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "tg_id": user.tg_id,
        "events": [{"id": e.id, "name": e.name, "date": e.date} for e in user.events]
    }


@router.post('/award_one_user')
async def award_one_user(session: SessionDep,
                     user=Depends(get_profile),
                     event=Depends(get_event_by_id)):

    async with session:
        user.balance += event.award
        await session.commit()
    return {'message': 'Пользователь успешно награжден'}


@router.post('/award_many_users')
async def award_many_users(session: SessionDep,
                     users_id: list[UserIDModel],
                     event=Depends(get_event_by_id)):
    async with session:
        for user in users_id:
            user = await UserDAO.find_one_or_none_by_id(session, model_id=user.id)
            if user is None:
                raise Exception(f'Пользователь с tg_id={user.id} не найден')
            user.balance += event.award
        await session.commit()
    return {'message': 'Пользователи успешно награждены'}


@router.post('/add_event_to_one_user')
async def add_event_to_one_user(session: SessionDep, event_id: int, user: SUser = Depends(get_profile)):
    '''Обязательно добавить чтобы пользователь уже не был участником мероприятия
    оно не работает. выдает ошибку
    sqlalchemy.exc.InvalidRequestError: A transaction is already begun on this Session.
    '''

    # print('start endpoint add_event_to_one_user')
    await EventParticipatedDAO.add(session, **{'users_id': user.id, 'events_id': event_id})
    return {'message': 'Мероприятие успешно добавлено в портфолио к пользователю'}


@router.post('/add_event_to_many_user')
async def add_event_to_many_user(session: SessionDep, event_id: int, users_id: list[UserIDModel]):
    '''Обязательно добавить чтобы пользователь уже не был участником мероприятия'''

    for user in users_id:
        # print(user.id)
        await EventParticipatedDAO.add(session, **{'users_id': user.id, 'events_id': event_id})
    return {'message': 'Мероприятие успешно добавлено в портфолио к пользователю'}


@router.post('/award_and_add_event_to_portfolio_many_users')
async def award_and_add_event_to_portfolio_many_users(session: SessionDep,
                                                      portfolio_info=Depends(add_event_to_many_user),
                                                      award_info=Depends(award_many_users)):
    if not portfolio_info['message'] == 'Мероприятие успешно добавлено в портфолио к пользователю':
        raise Exception(f'не получилось добавить мероприятие в портфолио')

    if not award_info['message'] == 'Пользователи успешно награждены':
        raise Exception(f'не получилось наградить пользователей')

    return {'message': 'Пользователи успешно награждены и мероприятие добавлено в портфолио'}


@router.post('/add_user')
async def add_user(user: SUserAdd, session: SessionDep):
    await UserDAO.add(session, **user.dict())
    return {'message': 'Пользователь успешно добавлен'}


@router.patch('/update_user')
async def update_user(tg_id: int, user: SUserUpdate, session: SessionDep):
    await UserDAO.update(session, filter_by={'tg_id': tg_id}, **user.dict())
    return {'message': 'Данные успешно обновлены'}


@router.delete('/delete_user')
async def delete_user(tg_id: int, session: SessionDep):
    await UserDAO.delete(session, tg_id=tg_id)
    return {'message': 'Пользователь успешно удален'}
