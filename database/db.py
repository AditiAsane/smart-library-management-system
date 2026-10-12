


from app.models.book import Book
from app.models.user import User


class LibraryDatabase:
    def __init__(self):
        self.users = {
            "U101": User(
                user_id="U101",
                name="Alice Johnson",
                role="Student",
            ),
            "U102": User(
                user_id="U102",
                name="Dr Robert Smith",
                role="Faculty",
            ),
        }

        self.books = {
            "B001": Book("B001", "Cloud Native DevOps Architecture", 5, 5),
            "B002": Book("B002", "Continuous Delivery Principles", 3, 3),
            "B003": Book("B003", "Clean Code", 4, 4),
            "B004": Book("B004", "Introduction to Algorithms", 3, 3),
            "B005": Book("B005", "Python Crash Course", 5, 5),
            "B006": Book("B006", "Designing Data-Intensive Applications", 2, 2),
            "B007": Book("B007", "Artificial Intelligence: A Modern Approach", 3, 3),
            "B008": Book("B008", "Computer Networking: A Top-Down Approach", 4, 4),
            "B009": Book("B009", "Operating System Concepts", 3, 3),
            "B010": Book("B010", "Database System Concepts", 4, 4),
            "B011": Book("B011", "The Pragmatic Programmer", 2, 2),
            "B012": Book("B012", "Hands-On Machine Learning", 3, 3),
        }

        self.borrowed_books = {}

    def reset(self):
        self.__init__()


db = LibraryDatabase()
