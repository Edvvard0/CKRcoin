import asyncio
import random
from sqlalchemy.orm import Session
from app.database import engine, get_session, SessionDep  # Импорт вашего подключения к базе данных
from app.users.dao import UserDAO
from app.users.model import User

# Имена и фамилии для генерации случайных пользователей
first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank", "Ivy", "Jack"]
last_names = ["Smith", "Johnson", "Brown", "Williams", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]


async def create_random_users():
    ''' Перед запуском этой функции надо добавить
    контекстный менеджер async with async_session_maker() as session:
    в basedao перед началом транзакции
    '''
    for _ in range(10):
        data = {
            'first_name' : random.choice(first_names),
            'last_name' : random.choice(last_names),
            'balance' : random.randint(0, 1000),  # Случайный баланс от 0 до 1000
            'tg_id': int(random.randint(10000, 99999)),  # Случайный Telegram ID
            'course' : random.randint(1, 5),  # Случайный курс от 1 до 5
            'group_id' : random.randint(1, 3),  # Случайная группа от 1 до 3
            'role_id' : 1,  # Роль у всех 1
            'secret_key' : None
        }
        session = SessionDep # Секретный ключ отсутствует
        await UserDAO.add(session=session, **data)


asyncio.run(create_random_users())
