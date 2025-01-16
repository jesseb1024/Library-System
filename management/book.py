class Book:
    def __init__(self, title, author, copies, genre, year, is_loaned=False, available=None, stat_manager=None):
        if not title or not author:
            raise ValueError("Title and author are required")
        if not isinstance(copies, int) or copies < 0:
            raise ValueError("Copies must be a non-negative integer")

        self.title = title.strip()
        self.author = author.strip()
        self.copies = copies
        self.genre = genre.strip()
        self.year = year
        self.is_loaned = is_loaned
        self.available = available if available is not None else copies
        self.stat_manager = stat_manager

    @property
    def key(self):
        from management.StatisticsManager import StatisticsManager  # Lazy import
        return StatisticsManager.generate_key(self.title, self.author)

    def borrow(self):
        """Borrow a book."""
        if self.available > 0:
            self.available -= 1
            if self.stat_manager:
                self.stat_manager.update_request_count(self.key)
            return True
        return False

    def return_book(self):
        """Return a borrowed book."""
        if self.available < self.copies:
            self.available += 1
            return True
        return False

    def to_dict(self, statistics_manager):
        """Convert the book details into a dictionary with request counts."""
        request_count = statistics_manager.get_request_count(self.key)
        waitlist = statistics_manager.get_waitlist(self.key)
        return {
            "Title": self.title,
            "Author": self.author,
            "Year": self.year,
            "Category": self.genre,
            "TotalCopies": self.copies,
            "AvailableCopies": self.available,
            "RequestCount": request_count,
            "waitlist": waitlist
        }

    def __str__(self):
        status = "Borrowed" if self.is_loaned else "Available"
        return f"{self.title} by {self.author} ({self.genre}), Status: {status}"
