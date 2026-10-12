import pytest

from app.services.library_service import LibraryService
from database.db import db


def test_borrow_and_return_book():
    result = LibraryService.borrow_book("U101", "B001")
    assert result["available_copies"] == 4

    result = LibraryService.return_book("U101", "B001")
    assert result["available_copies"] == 5


def test_cannot_borrow_same_book_twice():
    LibraryService.borrow_book("U101", "B001")
    try:
        with pytest.raises(ValueError, match="already borrowed"):
            LibraryService.borrow_book("U101", "B001")
    finally:
        LibraryService.return_book("U101", "B001")


def test_student_borrow_limit():
    db.borrowed_books["U101"] = ["B001", "B002", "B003"]
    try:
        with pytest.raises(ValueError, match="limit reached"):
            LibraryService.borrow_book("U101", "B001")
    finally:
        db.borrowed_books.pop("U101", None)
        db.books["B001"].available_copies = 5
        db.books["B002"].available_copies = 3
