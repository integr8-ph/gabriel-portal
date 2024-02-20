from src.exceptions import NotFound
from src.users.constants import UserNotFoundDetail


class UserNotFound(NotFound):
    DETAIL = UserNotFoundDetail.DETAIL
