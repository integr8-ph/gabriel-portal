import pytest

from src.auth.services import get_hashed_password, verify_password


class VerifyPassword:
    PARAMS = [
        ("test", get_hashed_password("test"), True),
        ("test", get_hashed_password("asd"), False),
        ("", get_hashed_password("a"), False),
    ]


class GetHashedPassword:
    PARAMS = [
        (
            "test",
            "asd",
        ),
        ("qwerty", "qwe"),
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize("params", VerifyPassword().PARAMS)
async def test_verify_password(params: VerifyPassword) -> None:
    plain, hashed, result = params
    assert verify_password(plain, hashed) == result


@pytest.mark.asyncio
@pytest.mark.parametrize("params", GetHashedPassword().PARAMS)
async def test_get_hashed_password(params: GetHashedPassword) -> None:
    first_pass, second_pass = params

    assert get_hashed_password(first_pass) != get_hashed_password(second_pass)
