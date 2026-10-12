from app.services.library_service import LibraryService


def test_seeded_books_exist():
    books = LibraryService.get_all_books()
    assert len(books) >= 2
    assert LibraryService.get_book("B001").available_copies == 5


def test_search_books():
    results = LibraryService.search_books("Cloud Native")
    assert any(book.book_id == "B001" for book in results)


def test_unknown_book_returns_none():
    assert LibraryService.get_book("UNKNOWN") is None
