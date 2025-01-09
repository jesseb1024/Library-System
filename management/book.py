class Book:

    def __init__(self, title, author, is_loaned, copies, genre, year, available):
        self.title = title
        self.author = author
        self.is_loaned = is_loaned
        self.copies = copies
        self.genre = genre
        self.year = year
        self.available = available



    def borrow(self):
        """Borrow a book."""
        if self.available > 0:
            self.available -= 1
            print(f"Borrowed '{self.title}'. Available copies: {self.available}")
        else:
            print(f"'{self.title}' is currently out of stock!")

    def return_book(self):
        """Return a borrowed book."""
        if self.available < self.copies:
            self.available += 1
            return True
        return False


    def to_dict(self):
        return {
            "Title": self.title,
            "Author": self.author,
            "Year": self.year,
            "Category": self.genre,
            "TotalCopies": self.copies,
            "AvailableCopies": self.available,
        }

    def generate_key(title, author):
        """Generates a normalized key for a book based on its title and author."""
        if not title or not author:
            raise ValueError("Both title and author are required to generate a key.")
        return f"{title.strip().lower()}:{author.strip().lower()}"

    def __str__(self):
        """
        Returns a user-friendly string representation of the book.
        """
        status = "Borrowed" if self.is_loaned else "Available"
        return f" {self.title} by {self.author} ({self.genre}), Status: {status}"




