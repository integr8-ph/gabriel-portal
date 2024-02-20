from src.exceptions import BadRequest, NotAuthenticated
from src.auth.constants import (
    InactiveDetail,
    InvalidUserOrPassDetail,
    NotSuperuserDetail,
)


class InactiveUser(BadRequest):
    DETAIL = InactiveDetail.DETAIL


class InvalidUserOrPass(NotAuthenticated):
    DETAIL = InvalidUserOrPassDetail.DETAIL


class NotSuperuser(NotAuthenticated):
    DETAIL = NotSuperuserDetail.DETAIL
