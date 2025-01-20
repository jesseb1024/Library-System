import logging


class Book:
    def __init__(self, title, author, year, copies, genre, available, is_loaned=False, request_counter=0):
        self.title = title
        self.author = author
        self.year = year
        self.copies = copies
        self.genre = genre
        self.is_loaned = is_loaned
        self.available = available  # Available copies
        self.request_counter = request_counter

    class Book:
        def __init__(self, title, author, is_loaned, copies, genre, year, available, request_counter):
            self.title = title
            self.author = author
            self.is_loaned = is_loaned
            self.copies = copies
            self.genre = genre
            self.year = year
            self.available = available
            self.request_counter = request_counter

        def to_dict(self):
            """Convert book details to a dictionary for saving to CSV."""
            return {
                "title": self.title,
                "author": self.author,
                "is_loaned": "yes" if self.is_loaned else "no",
                "copies": self.copies,
                "genre": self.genre,
                "year": self.year,
                "available": self.available,
                "request_counter": self.request_counter,
            }

    @classmethod
    def from_dict(cls, data):
        try:
            return cls(
                title=data["title"].strip(),
                author=data["author"].strip(),
                is_loaned=data["is_loaned"].strip().lower() == "yes",
                copies=int(data["copies"]),
                genre=data["genre"].strip(),
                year=int(data["year"]),
                available=int(data["available"]),
                request_counter=int(data["request_counter"]),
            )
        except (KeyError, ValueError) as e:
            logging.error(f"Invalid book data: {data} - {e}")
            return None

