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
        self.request_counter = request_counter  # Default to 0, but updated dynamically later

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
                title=data["title"].strip(),
                author=data["author"].strip(),
                year=int(data["year"]),
                copies=int(data["copies"]),
                genre=data["genre"].strip(),
                available=int(data["available"]),
                is_loaned=data["is_loaned"].strip().lower() == "yes",
                request_counter=request_counter,  # Dynamically fetched
            )
        except (KeyError, ValueError) as e:
            logging.error(f"Invalid book data: {data} - {e}")
            return None