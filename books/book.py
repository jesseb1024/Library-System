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
    def from_dict(cls, data, stat_manager):
        """Create a Book object from a dictionary using StatisticsManager."""
        try:
            # Generate the book key to fetch request counter dynamically
            book_key = stat_manager.generate_key(data["title"].strip(), data["author"].strip())
            request_counter = stat_manager.get_request_count(book_key)


            return cls(
                    title=data.get("title"),
                    author=data.get("author"),
                    is_loaned=data.get("is_loaned") == "yes",
                    copies=int(data.get("copies", 0)),
                    genre=data.get("genre"),
                    year=int(data.get("year", 0)),
                    available=int(data.get("available", 0)),
                    request_counter=int(data.get("request_count", 0))  # Map request_count
                )
        except (KeyError, ValueError) as e:
            logging.error(f"Invalid book data: {data} - {e}")
            return None