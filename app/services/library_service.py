from database.db import db


class LibraryService:
    STUDENT_BORROW_LIMIT = 3
    FACULTY_BORROW_LIMIT = 5

    @staticmethod
    def add_user(user):
        if user.user_id in db.users:
            raise ValueError("User already exists")
        db.users[user.user_id] = user
        return user

    @staticmethod
    def get_user(user_id):
        return db.users.get(user_id)

    @staticmethod
    def delete_user(user_id):
        if user_id not in db.users:
            raise ValueError("User not found")
        if db.borrowed_books.get(user_id):
            raise ValueError("Cannot delete a user with borrowed books")
        return db.users.pop(user_id)

    @staticmethod
    def add_book(book):
        if book.book_id in db.books:
            raise ValueError("Book already exists")
        db.books[book.book_id] = book
        return book

    @staticmethod
    def get_book(book_id):
        return db.books.get(book_id)

    @staticmethod
    def get_all_books():
        return list(db.books.values())

    @staticmethod
    def search_books(query):
        query = query.strip().lower()
        return [
            book for book in db.books.values()
            if query in book.title.lower()
            or query in book.book_id.lower()
        ]

    @staticmethod
    def borrow_book(user_id, book_id):
        user = db.users.get(user_id)
        book = db.books.get(book_id)

        if user is None:
            raise ValueError("User not found")
        if book is None:
            raise ValueError("Book not found")
        if book.available_copies <= 0:
            raise ValueError("No copies available")

        borrowed = db.borrowed_books.setdefault(user_id, [])
        role = user.role.strip().lower()

        if role == "student":
            limit = LibraryService.STUDENT_BORROW_LIMIT
        elif role == "faculty":
            limit = LibraryService.FACULTY_BORROW_LIMIT
        else:
            raise ValueError("Unsupported user role")

        if len(borrowed) >= limit:
            raise ValueError("Borrowing limit reached")
        if book_id in borrowed:
            raise ValueError("This book is already borrowed by this user")

        borrowed.append(book_id)
        book.available_copies -= 1

        return {
            "message": "Book borrowed successfully",
            "user_id": user_id,
            "book_id": book_id,
            "available_copies": book.available_copies,
        }

    @staticmethod
    def return_book(user_id, book_id):
        if user_id not in db.users:
            raise ValueError("User not found")

        borrowed = db.borrowed_books.get(user_id, [])
        if book_id not in borrowed:
            raise ValueError("This book is not borrowed by this user")

        borrowed.remove(book_id)
        db.books[book_id].available_copies += 1

        return {
            "message": "Book returned successfully",
            "user_id": user_id,
            "book_id": book_id,
            "available_copies": db.books[book_id].available_copies,
        }
