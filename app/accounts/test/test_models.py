import pytest

from app.accounts.models import User


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(email="test@example.com", password="secret")
    assert user.email == "test@example.com"
    assert user.check_password("secret")
