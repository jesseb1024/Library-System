import logging


class Book:
    def __init__(self, title, author, year, copies, genre, available, is_loaned=False, request_counter=0, waitlist=None):
        self.title = title
        self.author = author
        self.year = year
        self.copies = copies
        self.genre = genre
        self.is_loaned = is_loaned
        self.available_copies = available  # Available copies
        self.request_counter = request_counter
        self.waitlist = waitlist or []

    def to_dict(self):
        """Convert book details to a dictionary for CSV export."""
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "copies": self.copies,
            "genre": self.genre,
            "available": self.available_copies,
            "is_loaned": "yes" if self.is_loaned else "no",
            "request_counter": self.request_counter,
            "waitlist": ";".join(self.waitlist),
        }

    @classmethod
    def from_dict(cls, data):
        try:
            return cls(
                title=data['title'].strip(),
                author=data['author'].strip(),
                year=int(data.get('year', 0)),
                is_loaned=data.get('is_loaned', '').lower() == 'yes',
                copies=int(data.get('copies', 0)),
                genre=data.get('genre', '').strip(),
                available=int(data.get('available', 0)),
                request_counter=int(data.get('request_counter', 0)),
                waitlist=data.get('waitlist', '').strip("[]").split(';') if data.get('waitlist', '') else []
            )
        except (KeyError, ValueError, AttributeError) as e:
            logging.error(f"Invalid row in CSV: {data} - {e}")
            return None

