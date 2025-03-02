from fastapi import status, HTTPException


UserNoExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователя с таким тг id не существует'
)

GroupNoExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Группы с таким id не существует'
)