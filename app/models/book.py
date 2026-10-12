from dataclasses import dataclass


@dataclass
class Book:
    book_id: str
    title: str
    total_copies: int
    available_copies: int
