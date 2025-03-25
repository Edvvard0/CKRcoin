from fastapi import status, HTTPException


UserNoExistsException = lambda tg_id: HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f'User with this tg_id {tg_id} no find'
)

GroupNoExistsException = lambda group_id: HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f'Group with this group_id {group_id} no find'
)

TopUsersException = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail='Could not get top users'
)

UsersMyGroupException = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail='Could not find users for this group'
)


AddException = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail='Could not add data'
)
