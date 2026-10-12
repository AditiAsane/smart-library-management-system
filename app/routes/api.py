from dataclasses import asdict

from flask import Blueprint, jsonify, request

from database.db import db

from app.models.book import Book
from app.models.user import User
from app.services.library_service import LibraryService

api = Blueprint("api", __name__)

@api.get("/dashboard")
def dashboard():
    total_books = len(db.books)
    total_copies = sum(
        book.total_copies for book in db.books.values()
    )
    available_copies = sum(
        book.available_copies for book in db.books.values()
    )
    borrowed_count = sum(
        len(book_ids) for book_ids in db.borrowed_books.values()
    )

    return jsonify({
        "total_books": total_books,
        "total_copies": total_copies,
        "available_copies": available_copies,
        "registered_users": len(db.users),
        "currently_borrowed": borrowed_count,
    }), 200



@api.get("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@api.post("/users")
def create_user():
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    name = data.get("name")
    role = data.get("role")

    if not all(
        isinstance(value, str) and value.strip()
        for value in (user_id, name, role)
    ):
        return jsonify(
            {"error": "user_id, name and role are required"}
        ), 400

    user = User(
        user_id=user_id.strip(),
        name=name.strip(),
        role=role.strip(),
    )

    try:
        LibraryService.add_user(user)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 409

    return jsonify(asdict(user)), 201


@api.get("/users/<user_id>")
def get_user(user_id):
    user = LibraryService.get_user(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(asdict(user)), 200


@api.get("/books")
def get_books():
    query = request.args.get("search", "").strip()
    if query:
        books = LibraryService.search_books(query)
    else:
        books = LibraryService.get_all_books()
    return jsonify([asdict(book) for book in books]), 200


@api.post("/books")
def create_book():
    data = request.get_json(silent=True) or {}
    book_id = data.get("book_id")
    title = data.get("title")
    total_copies = data.get("total_copies")

    if not isinstance(book_id, str) or not book_id.strip():
        return jsonify({"error": "book_id is required"}), 400

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "title is required"}), 400

    if (
        isinstance(total_copies, bool)
        or not isinstance(total_copies, int)
        or total_copies < 1
    ):
        return jsonify(
            {"error": "total_copies must be a positive integer"}
        ), 400

    book = Book(
        book_id=book_id.strip(),
        title=title.strip(),
        total_copies=total_copies,
        available_copies=total_copies,
    )

    try:
        LibraryService.add_book(book)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 409

    return jsonify(asdict(book)), 201


@api.post("/borrow")
def borrow_book():
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    book_id = data.get("book_id")

    if not all(
        isinstance(value, str) and value.strip()
        for value in (user_id, book_id)
    ):
        return jsonify(
            {"error": "user_id and book_id are required"}
        ), 400

    try:
        result = LibraryService.borrow_book(
            user_id.strip(), book_id.strip()
        )
    except ValueError as exc:
        message = str(exc)
        status = (
            404
            if message in ("User not found", "Book not found")
            else 400
        )
        return jsonify({"error": message}), status

    return jsonify(result), 200


@api.post("/return")
def return_book():
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    book_id = data.get("book_id")

    if not all(
        isinstance(value, str) and value.strip()
        for value in (user_id, book_id)
    ):
        return jsonify(
            {"error": "user_id and book_id are required"}
        ), 400

    try:
        result = LibraryService.return_book(
            user_id.strip(), book_id.strip()
        )
    except ValueError as exc:
        message = str(exc)
        status = 404 if message == "User not found" else 400
        return jsonify({"error": message}), status

    return jsonify(result), 200
