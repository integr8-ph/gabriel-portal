from typing import NamedTuple

from pydantic import EmailStr


class OAuth2(NamedTuple):
    PAYLOADS = [
        ("user@example.com", "asd", 200),
        ("user@example.com", "qwe", 401),
        ("", "", 422),
    ]

    username: str
    password: str
    expected_status_code: int


class CreateUser(NamedTuple):
    PAYLOADS = [
        ("user55@example.com", "asd", True, 200),
        ("user@example.com", "asd", False, 409),
        ("user@invalidemail", "asd", True, 422),
        ("", "", True, 422),
    ]

    SUCCESSFUL_RESPONSE = {
        "email": "user55@example.com",
        "is_active": True,
        "is_superuser": True,
    }

    email: EmailStr
    password: str
    is_superuser: bool
    expected_status_code: int


class GetAllUsers:
    SUCCESSFUL_RESPONSE = [
        {
            "email": "user@example.com",
            "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$Zgdq59jQa9Mhlp6tvtbqKA$BblLTaprT9Q1jDoiefzzE2U7KBnEDXko1TsEEm1sWbk",  # noqa
            "is_active": True,
            "is_superuser": True,
            "created_at": "2024-02-20T06:24:30.704000",
        },
        {
            "email": "user1@example.com",
            "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$aydATrphk9devtlmh9RM6g$mNrtBz8GvFEHMz0w6bFImKsoHbWjijASkkHmV06RrqY",  # noqa
            "is_active": False,
            "is_superuser": False,
            "created_at": "2024-02-20T06:25:24.633000",
        },
        {
            "email": "user2@example.com",
            "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$bbBW5g7DdKEZzre+mXS3vA$VeZ2aM8OMY5N1w9Nh2NRmaFxPCJHKoWWEztivl1BpP8",  # noqa
            "is_active": True,
            "is_superuser": True,
            "created_at": "2024-02-20T10:12:19.145000",
        },
    ]


class GetUser(NamedTuple):
    PAYLOADS = [
        (
            "user@example.com",
            {
                "email": "user@example.com",
                "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$Zgdq59jQa9Mhlp6tvtbqKA$BblLTaprT9Q1jDoiefzzE2U7KBnEDXko1TsEEm1sWbk",  # noqa
                "is_active": True,
                "is_superuser": True,
                "created_at": "2024-02-20T06:24:30.704000",
            },
            200,
        ),
        (
            "user1@example.com",
            {
                "email": "user1@example.com",
                "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$aydATrphk9devtlmh9RM6g$mNrtBz8GvFEHMz0w6bFImKsoHbWjijASkkHmV06RrqY",  # noqa
                "is_active": False,
                "is_superuser": False,
                "created_at": "2024-02-20T06:25:24.633000",
            },
            200,
        ),
        ("user9999@example.com", {}, 404),
        ("user@invalidemail", {}, 422),
    ]

    email: EmailStr
    successful_response: dict
    expected_status_code: int


class UpdateUser(NamedTuple):
    PAYLOADS = [
        (
            "user55@example.com",
            "qwe",
            False,
            False,
            {
                "email": "user55@example.com",
                "is_active": False,
                "is_superuser": False,
            },
            200,
        ),
        ("user9999@example.com", "qwe", False, False, {}, 404),
        ("user@invalidemail", "qwe", False, False, {}, 422),
    ]

    email: EmailStr
    password: str
    is_active: bool
    is_superuser: bool
    successful_response: dict
    expected_status_code: int


class DeleteUser(NamedTuple):
    PAYLOADS = [
        (
            "user55@example.com",
            {
                "email": "user55@example.com",
                "is_active": False,
                "is_superuser": False,
            },
            200,
        ),
        ("user9999@example.com", {}, 404),
        ("user@invalidemail", {}, 422),
    ]

    email: EmailStr
    successful_response: dict
    expected_status_code: int
