from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from starlette import status

from app.database import SessionDep
from app.events.dao import EventParticipatedDAO
from app.events.router import get_event_by_id
from app.events.schemas import SEvent
from app.exceptions import (
    TopUsersException,
    UserNoExistsException,
    UsersMyGroupException,
)
from app.logger import logger
from app.users.dao import UserDAO
from app.users.model import User
from app.users.schemas import SUser, SUserAdd, SUserUpdate, UserIDModel

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def get_all_users(session: SessionDep) -> list[SUser]:
    logger.debug("Fetching all users")
    users = await UserDAO.find_all(session)
    logger.info(f"Retrieved {len(users)} users")
    return users


@router.get("/profile/{tg_id}")
async def get_profile(tg_id: int, session: SessionDep) -> SUser:
    extra = {"tg_id": tg_id}
    logger.debug("Fetching profile", extra=extra)

    user = await UserDAO.find_one_or_none(
        session, options=[selectinload(User.events)], **{"tg_id": tg_id}
    )

    if user is None:
        logger.warning("User not find", extra=extra)
        raise UserNoExistsException(tg_id)

    logger.info("Profile retrieved", extra)
    return user


@router.get("/top_10")
async def get_top_users(session: SessionDep):
    logger.debug("Fetching top users")
    top_users = await UserDAO.find_top_users(session)
    if not top_users:
        logger.error("Could not get top users")
        raise TopUsersException
    return top_users


@router.get("/users_my_group")
async def get_users_my_group(
    session: SessionDep, user: SUser = Depends(get_profile)
) -> list[SUser]:
    extra = {"group_id": user.group_id}
    logger.debug("Fetching users my group", extra=extra)

    users_my_group = await UserDAO.find_all(
        session, **{"group_id": user.group_id, "role_id": 1}
    )

    if not users_my_group:
        logger.warning("Could not find users for this group", extra=extra)
        raise UsersMyGroupException
    return users_my_group


@router.get("/portfolio/{tg_id}")
async def get_portfolio(session: SessionDep, user=Depends(get_profile)):
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "tg_id": user.tg_id,
        "events": [{"id": e.id, "name": e.name, "date": e.date} for e in user.events],
    }


@router.post("/award_users")
async def award_users(
    session: SessionDep, users_id: list[UserIDModel], event=Depends(get_event_by_id)
):
    async with session:
        for user_id in users_id:
            user = await UserDAO.find_one_or_none_by_id(session, model_id=user_id.id)
            if user is None:
                raise UserNoExistsException(user_id.id)
            user.balance += event.award
        await session.commit()
    return {"message": "Пользователи успешно награждены"}


@router.post("/events/{event_id}/participants")
async def add_event_participants(
    session: SessionDep, event_id: int, users_id: list[UserIDModel]
):
    logger.debug(f"Adding event_id={event_id} to users: {[u.id for u in users_id]}")
    for user in users_id:
        await EventParticipatedDAO.add(
            session, **{"users_id": user.id, "events_id": event_id}
        )
        logger.info(
            "Add new participant for event",
            extra={"event_id": event_id, "user_id": user.id},
        )
    logger.info(f"Event_id={event_id} added to {len(users_id)} users")
    return {"message": "Мероприятие успешно добавлено в портфолио к пользователю"}


@router.post("/events/{event_id}/award_and_add")
async def award_and_add_event_to_portfolio_users(
    users_id: list[UserIDModel],
    session: SessionDep,
    event: SEvent = Depends(get_event_by_id),
):
    logger.debug(
        f"Processing award and event addition for event_id={event.id}",
        f"and users: {[u.id for u in users_id]}"
    )

    awarded_users = 0
    added_events = 0

    try:
        for user_id in users_id:
            user = await UserDAO.find_one_or_none_by_id(session, model_id=user_id.id)
            if user is None:
                logger.warning(f"User with id={user_id.id} not found, skipping")
                continue

            existing = await EventParticipatedDAO.find_one_or_none(
                session, users_id=user.id, events_id=event.id
            )
            if existing:
                logger.warning(
                    f"User id={user.id} already participates in" +
                    f"event_id={event.id}, skipping event addition"
                )
            else:
                await EventParticipatedDAO.add(
                    session, **{"users_id": user.id, "events_id": event.id}
                )
                user.balance += event.award

                awarded_users += 1
                added_events += 1

        await session.commit()

        logger.info(
            f"Awarded {awarded_users} users with {event.award}" +
            f"and added event_id={event.id} to {added_events} portfolios"
        )
        return {
            "message": f"Successfully awarded {awarded_users}" +
            f"users and added event to {added_events} portfolios"
        }

    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {str(e)}", exc_info=True)

    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.post("/add_user", status_code=status.HTTP_201_CREATED)
async def add_user(user: SUserAdd, session: SessionDep):
    await UserDAO.add(session, **user.dict())
    return {"message": "Пользователь успешно добавлен"}


@router.patch("/update_user/{tg_id}")
async def update_user(tg_id: int, user: SUserUpdate, session: SessionDep):
    await UserDAO.update(session, filter_by={"tg_id": tg_id}, **user.dict())
    return {"message": "Данные успешно обновлены"}


@router.delete("/delete_user/{tg_id}")
async def delete_user(tg_id: int, session: SessionDep):
    await UserDAO.delete(session, tg_id=tg_id)
    return {"message": "Пользователь успешно удален"}
