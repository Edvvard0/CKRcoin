from app.dao.base import BaseDAO
from app.users.model import User, Group


class UserDAO(BaseDAO):
    model = User


class GroupDAO(BaseDAO):
    model = Group

