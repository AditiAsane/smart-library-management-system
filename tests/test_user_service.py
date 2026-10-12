from app.models.user import User
from app.services.library_service import LibraryService
from database.db import db


def test_get_seeded_user():
    user = LibraryService.get_user("U101")
    assert user is not None
    assert user.name == "Alice Johnson"


def test_add_and_get_user():
    user = User("U900", "Test User", "Student")
    LibraryService.add_user(user)
    assert LibraryService.get_user("U900") == user
    db.users.pop("U900", None)


def test_duplicate_user_rejected():
    try:
        LibraryService.add_user(User("U101", "Duplicate", "Student"))
        assert False, "Expected duplicate user to fail"
    except ValueError as exc:
        assert "already exists" in str(exc)
