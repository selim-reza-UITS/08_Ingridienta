import pytest

from app.accounts.models import User


@pytest.fixture
def user():
    return User.objects.create_user(email="user@example.com", password="pass")


def test_user_fixture(user):
    assert user.email == "user@example.com"
