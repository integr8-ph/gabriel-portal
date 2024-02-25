"""
List of Classes to parametrize each test function for routes
BASE PATTERN = PARAMS[(request_payload, status_code)]
"""

from tests.utils.utils import create_random_user


class CreateUser:
    PARAMS = [
        (create_random_user(), 200),
        (create_random_user(False), 409),
        (None, 422),
    ]
